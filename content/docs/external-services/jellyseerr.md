+++
title = 'Jellyseerr'
date = '2025-03-15T15:43:35Z'
draft = false
weight = 1
+++

# Jellyseerr
## Overview
[Jellyseerr](https://github.com/fallenbagel/jellyseerr), much like [Ombi](https://ombi.io/), is a media request system for the -arr services and Jellyfin/Emby/Plex. jfa-go integrates with Jellyseerr much better than it does with Ombi, and with fewer issues:
* Profiles for user & notification settings can be added in Settings > User Profiles
  * Like other profile data, admin can apply settings to a user manually from another user or profile with the "Modify Settings" feature in accounts.
* Creating accounts through jfa-go triggers Jellyseerr's user importer to create a "Jellyfin User", which like jfa-go uses Jellyfin as its authorization source, avoiding duplication and sync issues with the most important piece of data, the user's password.
  * If you already use Jellyseerr, make sure your users are "Jellyfin User"s, not "Local User"s! The latter will not be touched by jfa-go and passwords won't be synchronized.
* Email, discord and telegram details are synchronized, as are contact preferences for each.
  * Existing users can have these details migrated by enabling "Import existing users to Jellyseerr" for a while (shouldn't need to be left on once done).
* Disabled accounts are disabled in Jellyseerr (it does this on it's own, no credit taken here)

## Setup

Note this feature was merged on 31 July 2024, and a stable update has not been released since as of March 2025, so you'll need to use the unstable release.

* Enable in settings, supply a server URL and an API key, which you can get in the first tab of Jellyseerr's settings. Enable "Import existing users to Jellyseerr" to import data (contact methods) of your existing users, once everything appears to be done you can turn this setting off.

## FAQ

### Nothing's working!

Make sure you got the right API key. During Jellyseerr's setup they show you an API right after logging in to Jellyfin, **this is for Jellyfin, not Jellyseerr**! This is also shown in the "Jellyfin" tab in the programs settings. Make sure to **get the code from the first tab of settings**!.

### Accounts deleted in jfa-go/Jellyfin are still there on Jellyseerr!

Make sure your Jellyseerr users show as "Jellyfin user"s, not "Local user"s. The latter aren't managed by jfa-go. If they are local ones, you might be able to convert them, or just simply delete them and let the user log-in through their Jellyfin credentials.
