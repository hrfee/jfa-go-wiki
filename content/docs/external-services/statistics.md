+++
title = 'Statistics'
date = '2025-11-23T16:56:25Z'
draft = false
weight = 5
+++

# Statistics

jfa-go exposes a few API endpoints which you can use, along with your own code and means of storage and display, to track and visualize whatever's important to you. As some examples:
* Tracking the total number of users, number created through jfa-go or number created per day/week/month
* Monitoring how many users have accounts close to expiring, or how many accounts reach expiry before intervention (i.e. renewal)

## Endpoints

The API endpoints deemed useful for these sorts of things are tagged "Statistics" on [api.jfa-go.com](https://api.jfa-go.com/redoc/#tag/Statistics) (or on your own instances with the `-swagger` flag). As of 2025-11-23, these are available:

* `/activity[/count] [GET/POST]`: Probably the most useful, gets activities (or the number) of them matching any filters you provide. Most relevant things done by jfa-go are tracked in the activity log, so you can get a lot of information out of this.
* `/invites[/count[/used]] [GET]`: Get all stored invites, the number of them or the number of them that have been used at least once.
* `/users[/count] [GET/POST]`: Gets users, or the number of them, matching your filters or search terms.

## Filtering

The two filterable types of data, activities and users, are filtered the same way as in the web UI. Open up your browser's dev tools, go to the network tab, then create your search in the Accounts or Activity tab and press the search button to force a server-side search. A request to the relevant endpoint will then be created, from which you can observe the query format.

In this example, we're looking for any users created today. We'll do this by filtering for account creation activities which took place between yesterday at 23:59 and today at 23:59. Since the date parser on the web page is quite flexible, our search ends up as `time:"<today 23:59" time:">yesterday 23:59" account-creation:true`. Our filter request is sent off as so:

```json
{
  "searchTerms": [],
  "queries": [
    {
      "field": "time",
      "operator": "<",
      "class": "date",
      "value": {
        "year": 2025,
        "month": 10,
        "day": 23,
        "hour": 23,
        "minute": 59,
        "offsetMinutesFromUTC": 0
      }
    },
    {
      "field": "time",
      "operator": ">",
      "class": "date",
      "value": {
        "year": 2025,
        "month": 10,
        "day": 22,
        "hour": 23,
        "minute": 59,
        "offsetMinutesFromUTC": 0
      }
    },
    {
      "field": "accountCreation",
      "operator": "=",
      "class": "bool",
      "value": true
    }
  ],
  "limit": 20,
  "page": 0,
  "sortByField": "time",
  "ascending": false
}
```

![Filtering example](/filter.png)

## Script example (Python)

{{< code language="python" source="static/stats-example.py" options="linenos=inlines" >}}
