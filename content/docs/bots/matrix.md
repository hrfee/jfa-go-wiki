---
title: "Matrix Bot Setup"
date: 2024-08-10T18:40:17Z
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

As of commit [0445492](https://github.com/hrfee/jfa-go/commit/0445492), Matrix end-to-end encryption is fully functional, as the hard parts are now taken care of by (new to me) [cryptohelper](https://pkg.go.dev/maunium.net/go/mautrix/crypto/cryptohelper) package. When building with a Makefile, enable with `E2EE=on`. It can be enabled/disabled in the Matrix settings section, near the bottom. The path to the SQLite3 database used for encryption keys can be found in (Advanced) File Storage > Matrix encryption DB.

**However**, not all releases support it! The feature currently depends on the [go-sqlite3](https://wiki.jfa-go.com/docs/tls/) driver, which requires CGO and cross-compiling (and the associated toolchain headaches). Cross compilation is only done by the CI for certain architectures & OSes. If the setting appears missing for you, you'll have to compile it for yourself.
