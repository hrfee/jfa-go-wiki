---
title: "Adding Emails/Messages"
date: 2024-07-28T15:47:44+01:00
draft: false
weight: 2
---

# My (slightly improved) worst nightmare

Although this should be a bit more standardised than before ~[e67f1bf](https://github.com/hrfee/jfa-go/commit/e67f1bf1a988f58b48eb28e0db3a8b79fc795488), it's still quite confusing. This guide should help when adding new messages.

For an example, we're adding a new email to tell the user their dog ran away.

* Consider the inputs to your message, e.g. what's different between instances of the sent message. A common one is the username. jfa-go will replace variables with the "{var}" notation in any body text that you write, or the user writes in their customized version. Note that raw text and MJML/HTML email source files instead use "{{ .var }}" notation, and these variables represent language strings written in `lang/email/*.json` files instead, rather than input data. You can use the "{var}" notation within these strings themselves. For this email, we'll use three input variables:
  * `username`: The username of the recipient.
  * `ranAwayTime`: The time the recipient's dog ran away.
  * `location`: Where the dog was last seen. If not known, this is blank (keep that in mind).

* In `lang/email/en-us.json`, add a section for your email (called `dogRanAway`). Add a "name" field, which'll be the display name shown when a user wants to customize this message, and a "title" field, which'll be used as the email/message subject if applicable. Add variables for each distinct line/section of the email. If you have the means to, feel free to add translations. If your message is gonna take inputs (e.g. a username), you can use them in these strings with the "{var}" notation.
* In `lang.go`: Add the section to the `emailLang` struct (in CamelCase, i.e. `DogRanAway`).
* In `storage.go`: Add `DogRanAway` to the `customEmails` struct, and to the `patchLang` sections in `loadLangEmail`.
* In `mail/`, create `dog-ran-away.txt` and `dog-ran-away.mjml`, and define the structure of the email, trying to use *only* the variables you defined in `lang/email/en-us.json`.
  * For the MJML, you should base your work on other existing files, so the structure is similar.
  * The "{var}" notation inputs *will* be provided to the template, so a "{{ .var }}" would work, but this is only really intended for power-user customization.
* In `config/config-base.json`, define settings for the message/email subject (e.g. `[dog_running_away]/subject`), and for the paths to the email's html (**ending with `html`**) and message text (**ending with `text`**) (e.g. "email_html" and "email_text"). Their default value doesn't need to be set, as that information will be defined elsewhere.
* In `customcontent.go`, add an entry to the `customContent` map, with a key in CamelCase (e.g. `DogRanAway`). Set the entry roughly as follows. All fields are required unless stated as "OPTIONAL":
```go
var customContent = map[string]CustomContentInfo{
    // ...
    // Same CamelCase name we already decided on
    "DogRanAway": {
        // Same as the key
        Name: "DogRanAway", // Same as the key
        // Indicates this is a customizable message to be sent via chatbot or email,
        // rather than one to be shown in the app somewhere (CustomCard)
        // or to be used as a template for custom content to go into (CustomTemplate).
        ContentType: CustomMessage,
        // A function to return the display name of the message, which'll be shown to the user when customizing.
        // We'll reference the one we defined in the language store.
        DisplayName: func(dict *Lang, lang string) {
            return dict.Email[lang].DogRanAway["name"]
        },
        // A function to return the message/email subject line. Because custom subjects were added
        // before custom content, this value is generally a setting entry, rather than being stored 
        // in the database with the content.
        // Make sure to default to the "title" defined in the language store!
        Subject: func(config *Config, lang *emailLang) {
            return config.Section("dog_running_away").Key("subject").MustString(
                lang.DogRanAway.get("title")
            )
        },

        // OPTIONAL: A function to return some text to describe the purpose/context of the message
        // when the admin goes to customize this message.
        // Currently only used for the post signup card, which is a weird edge case anyway.
        Description: func(dict *Lang, lang string) string { return "leave me blank, probably!" }
        // OPTIONAL: A function to return the text to be shown in the header of message when sent as an HTML email.
        // This value is used in the `mail/layout/body-start.mjml` template partial.
        // If unset, defaults to serverHeader(), which returns "Jellyfin" or a custom name the user has set.
        // vendorHeader() is also available, returning "jfa-go".
        HeaderText: func(config *Config, lang *emailLang) string { return "leave me blank or use vendorHeader, probably!" }
        // OPTIONAL: A function to return the text to be shown in the footer of message when sent as an HTML email.
        // This value is used in the `mail/layout/body-end.mjml` template partial.
        // If unset, defaults to messageFooter(), which returns the "Help message" ([messages]/message) set by the user in settings.
        FooterText: func(config *Config, lang *emailLang) string { return "leave me blank, probably!" }

        // A []string of variable names. defaultVars() is a wrapper adding regularly used values.
        // As of writing, this includes just "username", but make sure to check near the top of customcontent.go.
        // Since "username" is already included, we'll just add the two remaining:
        Variables: defaultVars(
            "ranAwayTime",
            "location",
        ),
        // A map of variables to the placeholder value (to be Sprintf-ed) shown when the user is customizing the message.
        // defaultVals() includes placeholder values for stuff included in defaultVars().
        Placeholders: defaultVals(map[string]any{
            "ranAwayTime": "01/01/25 08:00",
            "location": "Beckenham Place Park",
        }),

        // OPTIONAL:  A []string of variable names that should also behave as conditionals,
        // letting the user test their truthiness and show/hide text based on it.
        // In this example, the user could now do something like this: 
        // {if location}They were last seen at {location}.{endif}{if !location}We don't know where they last were.{endif}
        Conditionals: []string{
            "location",
        },

        // Along with customizing the content of messages in the app, users can also provide custom HTML and text files
        // via a pair of settings entries, one for "text" and one for "html". These should be advanced settings.
        SourceFile: ContentSourceFileInfo{
            // Settings section.
            Section: "dog_running_away",
            // Prefix of the two settings: With this value, they -must- be called "email_html"/"email_text".
            SettingPrefix: "email_",
            // The base filename you used for the MJML and TXT files you wrote earlier (without the ".mjml"/".txt").
            DefaultValue: "dog-ran-away",
        },
    },
    // ...
}
```
* In `email.go`, you'll now need to write a message constructing function, roughly like this:
```go
func (emailer *Emailer) constructDogRanAway(username string, ranAwayTime time.Time, location string, placeholders bool) (*Message, error) {
    // When the message editor ui needs a copy of the message content for the user to base theirs on,
    // this function is called with placeholders=true. This tells the function to make sure all {var}-type variables to be left untouched, i.e. to be left in the message as {var}. You could also do this by only templating the string if placeholders=false, or by templating with "{var}". For things like username, it can be nicer to do the latter.
    ranAwayTimeString := formatDatetime(ranAwayTime) // Format to a nice looking string
    if placeholders {
        username = "{username}"
        ranAwayTimeString = "{ranAwayTime}"
        location = "{location}"
    }

    // Here we'll plug in -all- the variables: The language strings, and the input variables.
    // If you used any input variables in your language strings, you should put them here. If you used an "if placeholders" block like above, you can template them here, if not, put the un-templated form here and do it later in an "if !placeholders" block.
    // If your message doesn't use the assumed-included username variable, just leave it blank.
    contentInfo, template := emailer.baseValues("DogRanAway", username, placeholders, map[string]any{
        // language string variables
        "helloUser": emailer.lang.Strings.template("helloUser", tmpl{"username": username}),
        "yourDogRanAwayAtTime": emailer.lang.DogRanAway.template("yourDogRanAwayAtTime", tmpl{"ranAwayTime": ranAwayTimeString}),
        // note for this one: we'll evaluate our own conditional further down.
        "lastSeenAt": emailer.lang.DogRanAway.template("lastSeenAt", tmpl{"location": location}),

        // input variables (excluding "username", that's already done for us)
        "ranAwayTime": ranAwayTimeString, 
        "location": location, // Might be blank, that's fine.
    })

    if !placeholders {
        // Our html/text version of the email has a conditional, which we evaluate here.
        if location == "" {
            template["lastSeenAt"] = emailer.lang.DogRanAway.get("notLastSeen")
        }
    }

    // If the user wrote the own custom version of the message, grab it (note contentInfo.Name == "DogRanAway")
    cc := emailer.storage.MustGetCustomContentKey(contentInfo.Name)
    // Construct and return the message
    return emailer.construct(contentInfo, cc, template)
}
```

* In `api-messages.go`, in the large `switch id {` block in the `GetCustomMessageTemplate()` function, add a case for "DogRanAway", calling your new constructing function with blank values, and with `placeholders=true`:
```go
// ...
    case "DogRanAway":
        msg, err = app.email.constructDogRanAway("", time.Time{}, "", true)
// ...
```
* Go and use the message through your new constructing function!

That should be all, however this process has changed a lot and the instructions might be incomplete.
