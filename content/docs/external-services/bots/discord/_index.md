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
![paste here](/discord/7_2.jpg)

## 8) Grant the bot instance its permissions

You'll next need to make sure the bot's role (which itself creates) has the correct rank and permissions.
Open server settings by opening your server, clicking the name in the top left and selecting "Server settings":

![server dropdown](/discord/serverdropdown.webp)

From the newly-shown sidebar, go to the "Roles" section. If you want jfa-go to apply a specific role to users who have signed up, you'll need to drag your bot's role (probably "<Your Bot Name> role") **above** that role. A drag-anchor will appear on the left when you hover over it. Also, if you face any issues with the bot, try dragging it right to the top, and lowering it until your issues come back.

![roles page](/discord/rolespage.webp)

Once it's in the right place, click the edit icon on the role to bring up a new page. Select the "Permissions" tab as shown:

![bot perms tab](/discord/botperms.webp)

In this list, enable the following permissions (if they aren't already):
* View Channels
* Manage Roles
* Create Invite (If you want an invite to be shown on the invite form)
* Send Messages
* Embed Links
* Use Application Commands

Make sure to press **"Save Changes"** after!

If you face any further issues, check your jfa-go logs and look for permissions errors, they often have a description of the missing permission which you can then come here to enable.

## 9) Done!
Once you've restarted, you should be able to add new users in the Account tab, and link your discord on the sign-up page. You can also tell jfa-go to assign a discord role to new users in Settings > Discord (make sure you've made your role and put it in the right position in the above described list).
