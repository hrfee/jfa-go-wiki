---
title: "FAQ"
date: 2021-06-23T17:30:30+01:00
draft: false
weight: 10
---

## Jellyfin says "Try again within your home network" when trying to reset password 

([issue](https://github.com/hrfee/jellyfin-accounts/issues/12))

* The best way to get around this (if you're using a reverse proxy) is to selectively not send the users real IP to jellyfin on the paths that are used for password resets. Read more and see an example [here]({{<relref "/docs/pwr/remote-network" >}}).

* Another method is to tell Jellyfin to treat all traffic as local. I don't recommend this as it stops you from using other features like remote bandwidth limiting. In Jellyfin, go to Dashboard > Networking (under Advanced), and set the 'LAN networks' setting to `0.0.0.0/0`.

## I can't access `localhost:8056`

jfa-go does not run as a daemon, so if you aren't using a service manager to achieve this, you need to run `jfa-go` in a terminal and keep it open. If you're on linux and wish to use systemd, run the below command to get a `.service` file:
```shell
$ jfa-go systemd
To start: If you want to execute jfa-go with special arguments, re-run this command with them.
Move the newly created "jfa-go.service" file to ~/.config/systemd/user (Creating it if necessary).
Then run "systemctl --user daemon-reload".
You can then run:

To start: "systemctl --user start jfa-go"

To stop: "systemctl --user stop jfa-go"

To restart: "systemctl --user restart jfa-go"
```

## I closed jfa-go during setup, and now it's broken/i can't get back to it.

Post v0.3.7, this should no longer be an issue.

Try deleting the config directory. When you first run jfa-go, it will print something like this:
```
[INFO] 21:39:40 Copied default configuration to "/tmp/jfa-go/config.ini"
```
In this case, `/tmp/jfa-go` is the config directory. Delete it, and run the program again to start setup again.

If you're using a build with a tray icon, you won't see this message, so here's some common paths:
* Linux: `~/.config/jfa-go/config.ini`
* Windows: `C:\Users\<your username>\AppData\Roaming\jfa-go\config.ini`
* macOS: `~/Library/Application Support/jfa-go/config.ini`

## GMail isn't working.

There's a lot of possibilities for this, but the most common seems to be the use of a VPN. Read through [this](https://support.google.com/mail/answer/7126229#zippy=%2Ci-cant-sign-in-to-my-email-client) google support article, and [both](https://github.com/hrfee/jellyfin-accounts/issues/15) of [these](https://github.com/hrfee/jfa-go/issues/3) issues before you open one.

**My other email provider isn't working.**

Make sure to check the ports you are using, as generally they correspond to the protocol used by the provider (465 for normal SSL/TLS, and 587 for STARTTLS). Also note that some new email providers don't provide SMTP access, or require a subscription for access. In this case just shop around for another email provider.

## jfa-go starts before Jellyfin, and then crashes.

This should be unlikely to happen post [f6fdd41](https://github.com/hrfee/jfa-go/commit/f6fdd41b35ec30b56f79690a288eff9575f8fa07), but if it does, you can increase the number of tries jfa-go makes to connect to Jellyfin before failing. In Settings > Advanced, increase the "Initial auth retry count" or "Initial auth retry gap (seconds)" until jfa-go waits long enough.

## I set up the Ombi integration, now i'm locked out of Ombi.

Sorry if this has occurred, you can regain access by following [the guide here]({{<relref "/docs/external-services/ombi" >}}).

## Does this need to be installed on the same host as Jellyfin?

Not necessarily. For invite functionality, an http connection is only necessary. Password resets through the "User Page" Feature will also function, see [this note](/docs/pwr/#method-4-my-account-reset). However, password resets through the Jellyfin UI require jfa-go to be able to access its config directory, so you'll need to use SMB or similar to mount it. See [this page](/docs/pwr/#prerequisite-for-methods-1-3) for help finding the correct directory.

## Can i `go get` this repository?
No, because the supporting files (CSS, email templates, etc.) need to be compiled and placed next to the executable before it will run, and `go get` will only compile the app itself.

