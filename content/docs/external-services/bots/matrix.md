---
title: "Matrix"
date: 2024-08-10T20:13:59Z
draft: false
---

# Matrix bot setup

To use the Matrix integration, you must create a normal Matrix account for jfa-go to log in to. If you already have one you'd like it to use, skip step 1. This one's not too difficult but not as easy as Telegram.

## Normal method

This is the easier method, but is sometimes a little iffy. I recommend you try it first.

### 1) Create a bot account

Visit [app.element.io](https://app.element.io), and press "Create account".

![signup page](/matrix/1.png)

If you wish to use a different matrix home server, you can change it here. Make sure to remember it for later.

![signing up](/matrix/2.png)

### 2) Add it to jfa-go

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
1) Log in to the account through element.io.
2) Click the dropdown next to your username on the top left and press "All settings".
3) Select "Help & About" on the right, and scroll down to the Advanced section. 
4) Click the dropdown next to "Access token", and copy the token.
5) In jfa-go, go to Settings > Matrix. Enable it, and paste the access token into the token box. Add your home server and user ID, then apply.

## End-to-end encryption

As of commit [69569e](https://github.com/hrfee/jfa-go/commit/69569e) (Committed 10th August 2024), Matrix end-to-end encryption is fully functional, as the hard parts are now taken care of by the (new to me) [cryptohelper](https://pkg.go.dev/maunium.net/go/mautrix/crypto/cryptohelper) package. When building with a Makefile, enable/disable with `E2EE=on/off`. It can be enabled/disabled in the Matrix settings section, near the bottom. The path to the SQLite3 database used for encryption keys can be found in (Advanced) File Storage > Matrix encryption DB.

**However**, not all releases support it! The feature currently depends on the [go-sqlite3](https://wiki.jfa-go.com/docs/tls/) driver and `libolm` library, which require CGO and cross-compiling (and the associated toolchain headaches), and the latter a runtime dependency. Cross compilation is only done by the CI for certain architectures & OSes. If the setting appears missing for you, look for an alternative on [dl.jfa-go.com](https://dl.jfa-go.com), or compile it for yourself.
