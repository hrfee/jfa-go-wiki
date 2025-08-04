---
title: "Adding Emails/Messages"
date: 2024-07-28T15:47:44+01:00
draft: false
weight: 2
---

# My worst nightmare

I wrote this so I can maintain sanity next time I have to do it, but for anyone else who is adding a new email/message type to jfa-go, these notes might help.


For an example, we're adding a new email to tell the user their dog ran away.

It roughly goes:
* In `lang/email/en-us.json`, add a section for your email (called `dogRanAway`), add variables for each line/section of the email. If you have the means to, feel free to add translations.
* In `lang.go`: Add the section to the `emailLang` struct (in CamelCase, i.e. `DogRanAway`).
* In `storage.go`: Add `DogRanAway` to the `customEmails` struct, and to the `patchLang` sections in `loadLangEmail`.
* In `mail/`, create `dog-ran-away.txt` and `dog-ran-away.mjml`, and define the structure of the email, using the variables you defined in `lang/email/en-us.json`, or some custom variables you'll pass in the next step.
* In `email.go`: Define two functions: `dogRanAwayValues`, and `constructDogRanAway`, following the function of the others in there. Make sure the variables you pass to the templater match what you put in `mail/`. Make sure to reference the paths provided by the settings you'll add in the next step.
* In `config/config-base.json`, define settings for the email subject, html and text email paths. (i.e. `[dog_ran_away_section] -> subject/email_html/email_text`)
* In `config.go`, find the bit where there's lots of `email_html` and `email_text`: Copy one of the pairs of `app.MustSetValue` calls and change it to conform to the settings from the previous step, setting the default values to `"jfa-go:"+"dog-ran-away.html/txt"`.
* In `api-messages.go`:
  * In `GetCustomContent`, add a line to the `emailListDTO` for `DogRanAway`.
  * In `GetCustomMessageTemplate`, add a case for `DogRanAway` to the big switch statement, calling the two functions you defined in `email.go`. Pass `dogRanAwayValues` some bogus values to be shown when the user edits the email.
* In `migrations.go`, add a block to `initialiseCustomContent` to create an empty custom content entry for `DogRanAway`, following the same format as all the others.

Then use `constructDogRanAway` to create the email where needed.

