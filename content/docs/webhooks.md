---
title: "Webhooks"
date: 2024-08-20T19:13:44Z
draft: false
---
# Webhooks

jfa-go can send HTTP requests to let other software know when things happen. Any number of target URLs can be added for each category in Settings > Webhooks. Data is usually passed along in the form of a JSON object. Most of these should be documented in the [API Docs](https://api.jfa-go.com) as return types.

## Account Creation
Pinged when an account is created through jfa-go. Passes a `respUser` object, similar to that returned by [GET /users](https://api.jfa-go.com/redoc/#tag/Users/paths/~1users/get).

Note that not all account tasks may have been completed when the request is sent, so some fields like Discord ID or Referral status may not be populated in the response object. If you need these, Acquire them yourself with [GET /users](https://api.jfa-go.com/redoc/#tag/Users/paths/~1users/get) after waiting a couple seconds.
