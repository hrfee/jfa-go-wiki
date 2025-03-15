---
title: "Ombi"
date: 2023-10-04 12:22:19.000000000 +0100
draft: false
weight: 2
---

# Ombi
## Warning
The Ombi integration has a frustrating issue that has locked at least 2 people out of their Ombi admin account. Despite my best efforts, I have not been able to find the cause. **If you wish to use this integration, I recommend setting up backups of your Ombi database**. It might also be wise to try out [Jellyseerr](https://github.com/fallenbagel/jellyseerr) and see if you prefer it, the [jfa-go integration]({{<relref "/docs/external-services/jellyseerr" >}}) is much better.

In the event that you experience the bug and do not have a recent backup, you can use the API key you gave jfa-go to create a new Admin account, from which you can reset your personal one:
1) Visit `ombi-address:port/swagger`.
2) Scroll down to the `POST /api/v1/Identity` entry, and click the lock icon.


![lock icon](/ombi-swagger-auth.png)

2) Copy the Ombi API key you gave jfa-go from the settings, and paste it into the window that popped up when clicking the lock icon, and then click Authorize.

![jfa-go key](/ombi-jfa-go-key.png)

![swagger key](/ombi-swagger-key.png)

3) In the dropdown below `POST /api/v1/Identity`, click the **"Try it out"** button, and in the textbox above the "Execute" button, enter the following, editing to match what you wish:
```json
{
    "userName": "your-username",
    "claims": [
        {
            "value": "Admin",
            "enabled": true
        }
    ],
    "password": "your-password"
}
```
4) Click execute. An admin user will be created with the username and password you specified. 
5) Login to this new Ombi user, and use it to regain access to your original account (i.e. Change the password and/or username back).
6) When done, delete this user (or keep it, in case this happens again).
