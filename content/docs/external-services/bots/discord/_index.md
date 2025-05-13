---
title: "Discord"
date: 2021-06-23T17:30:30+01:00
draft: false
weight: 1
---

# Discord bot setup

To use the Discord integration, you must create a Discord bot through their developer portal with the correct permissions, then add it to your server, as described below. This is probably the hardest bot to set up, but has the most features.

## 1) Create an application
Visit [discord.com/developers](https://discord.com/developers) and log in. Press the "New Application" Button, enter a name, and press "Create".

![new app](/discord/1.jpg)

## 2) Go to the Bot tab
You can leave the settings on this page alone. Open the side menu (if necessary), and open the "Bot" tab.

![bot tab](/discord/2.jpg)

## 3) Create the Bot
Press the "Add Bot" button, and "Yes, do it!" to create the bot.

![add bot](/discord/3.jpg)

## 4) Enable privileged permissions
jfa-go needs the privileged intent "Server Members" to present a list of users when you try to bind an existing Jellyfin account to a Discord one. Scroll down on the bot summary page to the "Privileged Gateway Intents" section, enable the "Server Members Intent", then press "Save Changes" when it pops up.

![privileged permissions](/discord/4.jpg)

## 5) Switch to the OAuth2 Tab
Open the side menu (if necessary), and open the "OAuth2" tab.

![oauth2 tab](/discord/5.jpg)

## 6) Enable permissions, get Invite link
Scroll down the page to the "Scopes" section, check all the checkboxes shown below, and save. Once done, press the "Copy" button below the Client ID to copy it. **Replace the `YOUR_CLIENT_ID` in the below link and visit it to add the bot to your desired Discord server.**

```url
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=2415938561&scope=applications.commands%20bot
```


![bot permissions](/discord/6.jpg)

## 7) Copy the token
Switch back to the "Bot" tab, and press the "Copy" button to copy the bot token. In jfa-go, go to Settings > Discord, enable it, and paste the token into the "API Token" box. Save and restart.

![copy token](/discord/7.jpg)
![paste here](/discord/8.jpg)

## 8) Done!
Once you've restarted, you should be able to add new users in the Account tab, and link your discord on the sign-up page.
