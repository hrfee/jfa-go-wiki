---
title: "Discord FAQ"
date: 2022-01-13T22:40:18+01:00
draft: false
---

# Discord FAQ

### How do i setup slash commands?

If you've followed the setup process recently, this should work by default. If not, you'll need to go through the setup process again starting from step 6. You'll also need to kick and re-add your bot using the new link.

### How does this work?

* There is a `Link Discord` button on the sign-up form. When clicked, the user is given a short PIN code (e.g. `AB-CD-EF`).
* If the user is already a member of your Discord server, they send `/start` (or your own command) to the channel you set in "Settings > Discord > Channel to monitor". If they aren't a member, you can enable "Provide server invite" in settings to display an invite next to the PIN.
* After sending the start message, they are asked to send `/pin <PIN>` where PIN is the one shown on the form. Once they send it, they return to the sign-up form.
* Once the user has signed up, notifications, password resets, announcements and such can be sent to them via Discord.

You can also connect a Discord user to a Jellyfin account in the Accounts tab if the user's already signed up.

### Applying a role when the user signs up

You can enable this in Settings > Discord > Apply role on connection. For this to work, make sure:
* Your bot has the "Manage Roles" permission (If set up before 13th January 2021, you'll need to do this and re-add the bot to your server)
* Your bot's role is higher in the role hierarchy than the role you're applying (You can do this in Discord's role settings by dragging the bots role upwards)
  * To clarify, take this example: Your bot has the role `bots`, and you want to apply the role `member` to new users. In Discord's role settings, make sure `bots` is above `member`.


