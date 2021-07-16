---
title: "Matrix Bot Setup"
date: 2021-06-23T17:30:30+01:00
draft: false
---

# Matrix bot setup

The Matrix bot uses a normal account, so you can create it however you choose. If you already have an account made for the bot, skip step 1.

## Normal method

### 1: Create a bot account

Visit [app.element.io](https://app.element.io), and press "Create account".

![signup page](/matrix/1.png)

If you wish to use a different matrix home server, you can change it here. Make sure to remember it for later.

![signing up](/matrix/2.png)

### 2: Add it to jfa-go

Go to Settings and press the "+" button next to Matrix.
* If you can't see it, make sure messages/notifications are enabled, and matrix is disabled. 
* **If you already have an access token, enable matrix and fill in the details yourself**.

![link matrix button](/matrix/3.png)
![linking matrix to jfa-go](/matrix/4.png)

Fill in the:
* Home server address (If you used the default on element.io, this will be `https://matrix.org`.)
* Username (`@<your username>:<your homeserver>`), for example, `@jfa-bot:matrix.org`.
* Password

then press submit. The app will restart and the page will refresh. Matrix should now be enabled.
You can link Chat IDs with existing Jellyfin users in the accounts tab, and users should be able to link them on the sign-up page.

## Alternate method

If adding your account through the wizard in jfa-go doesn't work, you can get the required access token yourself. 
* Login to the account through element.io.
* Click the dropdown next to your username on the top left and press "All settings".
* Select "Help & About" on the right, and scroll down to the Advanced section. 
* Click the dropdown next to "Access token", and copy the token.
* In jfa-go, go to Settings > Matrix. Enable it, and paste the access token into the token box. Add your home server and user ID, then apply.

## End-to-end encryption

There is very experimental support for end-to-end encryption, however you must compile jfa-go manually to enable it with `make all E2EE=on`. After compilation, checking "Advanced settings" in Settings will show a toggle for it under the Matrix section. Receiving messages is currently broken, so the `!lang` command will not work for users. 

If you have any know-how on implementing this in any language (preferably with one of the `mautrix` libraries), help would be appreciated.
