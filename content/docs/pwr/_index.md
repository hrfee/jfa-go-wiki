---
title: "Password Resets"
date: 2023-09-09T13:32:35+01:00
draft: false
weight: 15
---

## Password Reset Methods
There are 4 main methods for facilitating password resets. They are ordered from (in my opinion, at least) worst to best, although your choice will depend on your situation.. They are described below:
1) **Through Jellyfin (PIN Reset)**: The user clicks "Forgot Password" on the Jellyfin login screen, and enters their username. Jellyfin generates a file with a PIN code. Jfa-go reads this file, and sends the PIN to any contact methods associated with the user (Email, Discord, Matrix or Telegram). The user then types this PIN when Jellyfin asks for it.
2) **Partially through Jellyfin (Link Reset)**: Similarly to above, the user clicks "Forgot Password" and enters their username. Jfa-go reads the file with the PIN, but instead sends the user a link that will automatically set their password to the PIN, as Jellyfin would if they typed it in.
3) **Partially through Jellyfin (Internal Reset)**: Same as above, but the link sent to the user takes them to a special jfa-go password reset page.
4) **Through Jfa-go (User Page/"My Account" Reset)**: The user visits the "My Account" page (`your-jfa-go.site/my/account`), and presses the "Forgot Password" button. They enter their Jellyfin username, or address/ID of a contact method (email address or discord/telegram/matrix username). A message with a link is sent, which links to the same password reset page described in method 2.

## Pros/Cons

{{< include-html "static/pwr/pwr-pros-cons.html" >}}

## Setting them up

### Prerequisite for Methods 1-3
jfa-go will need access to your Jellyfin config directory, as this is where it places the files containing PINs.
  * General Advice: When initiating a password reset in Jellyfin, a message will pop up telling you the location the PIN file was created in. This is the easisest way to find the directory. However, this feature was [broken in older versions](https://github.com/jellyfin/jellyfin/issues/6093) and still is for some.

![PWR Directory Screenshot](/pwr-directory.png)


  * Docker: The directory you mounted to `/config` in the container, e.g. for `docker create ... -v /opt/jellyfin:/config`, the config directory would be `/opt/jellyfin`.
    * If you're also running jfa-go in docker, make sure to mount it to `/jf` within the container; jfa-go should default to that path.
  * Windows: The directory should be `C:\ProgramData\Jellyfin\Server` or similar.
  * Ubuntu/Debian: Should be `/var/lib/jellyfin`, or one of it's sub-directories. initiate a Password Reset and look for a file beginning with `passwordreset` to confirm.

### Method 1 (PIN Reset)

* Enable Password Resets in settings, that's all.

### Method 2 (Link Reset)

* Enable Password Resets, and in the same section, enable *"Use reset link instead of PIN"*.

### Method 3 (Internal Reset)

* Enable both the settings for the above 2 methods, and also enable *"Set password through link"*.

### Method 4 ("My Account" Reset)

* Enable all of the settings listed above.
* Enable the *User Page* feature.
* Ensure *Use Jellyfin for Authentication* in *General* is enabled.

* **Note**: Despite enabling the above features, jfa-go **does not need access** to the Jellyfin config directory if you only want this method to be used. You can point the directory to wherever, it doesn't matter.

## Additional Suggestions

The prompt given by Jellyfin (*"The following file has been created..."*) doesn't explain to the user that they need to check their email/contact method, and if using Link or Internal resets, you ideally don't want the Enter PIN page to show at all. 

[This comment by @Rezer](https://github.com/hrfee/jfa-go/issues/240#issuecomment-1779875680) gives some suggestions on how to customize Jellyfin's HTML and CSS to avoid such references, and even point directly to "My Account" so resets only happen through jfa-go. Issue [#327](https://github.com/hrfee/jfa-go/issues/327) May also have some helpful information.

Additionally, [@BobHasNoSoul](https://github.com/BobHasNoSoul)'s [jellyfin-mods](https://github.com/BobHasNoSoul/jellyfin-mods) list contains lots of guides for customizing Jellyfin in general which you might find useful.
