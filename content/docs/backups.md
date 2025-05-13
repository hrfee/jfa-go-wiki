---
title: "Backups"
date: 2023-12-21T21:17:20+01:00
draft: false
weight: 30
---

# Database Backups

Bugs may occasionally cause issues with jfa-go, and occasionally these issues are destructive. A built-in backup feature has been added to help mitigate any damage.

Visit Settings > Backups to enable scheduled backups, set the frequency of the backups (every *n* minutes), and the number of most recent backups to keep.

Data corruption might happen after an update, so it's wise to keep a backup from the previous version. Enable "Keep 1 backup from each previous version" to do so. The "keep n backups" option will delete the oldest per-version backups but leave the most recent one.

## List backups
Press the "Backups" button at the top of Settings. A list of all stored backups will be shown.

## Manually make a backup
Press the "Backups" button, and press "Backup Now" in the window that appears.

## Restore from a backup

### From the Web UI
Press the "Backups" button. 
* If the `.bak` file you wish to use is available in jfa-go, locate it and press the red "Restore" button to its right.
* If the `.bak` file is located on your device, press "Upload Backup" and select it.

The restore should only take a few seconds. Refresh the page to see the result.

### From the console
In case your jfa-go won't start, you can restore backups through the command line.

If you haven't got a `.bak` file, you should be able to find them in `<your data directory>/backups`, for example:
* Linux: `~/.config/jfa-go/backups`,
* Windows: `C:\Users\<your username>\AppData\Roaming\jfa-go\backups`,
* macOS: `~/Library/Application Support/jfa-go/backups`
* Docker: `/data/backups`

Once you've found a file, simply run `<your usual jfa-go start command> -restore <bak file path>`.
The application will start normally after the restore has completed.

