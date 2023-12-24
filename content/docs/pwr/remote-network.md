---
title: "Password Resets outside local network"
date: 2021-06-23T17:30:30+01:00
draft: false
---

# Password resets outside local network

If you have Jellyfin set up to recognize connections from the LAN network, it will complain when a user tries to do a password reset remotely:

![please try again within your home network](/pw-localnetwork.png)

If you're using a reverse proxy, Jellyfin knows the real IP of a user through the `X-Forwarded-For` HTTP header, which common proxy configs include. If you want to allow password resets for remote users, you can selectively override this with an IP address the Jellyfin sees as local for the necessary routes, which are `http://<jellyfin address>/Users/ForgotPassword` and `http://<jellyfin address>/Users/ForgotPassword/Pin`.

***Example NGINX config***
```nginx
    # add to your `server { ... }` block

    # rest of jellyfin config

    location /Users/ForgotPassword {
        proxy_pass http://<jellyfin address>/Users/ForgotPassword;
        proxy_set_header X-Forwarded-For <any local ip address>;
    }

    location /Users/ForgotPassword/Pin {
        proxy_pass http://<jellyfin address>/Users/ForgotPassword/Pin;
        proxy_set_header X-Forwarded-For <any local ip address>;
    }
```

***Example Caddy config*** (from [#133](https://github.com/hrfee/jfa-go/discussions/133), Credit to [robocrax](https://github.com/robocrax))
```Caddyfile
jellyfin {

    # rest of jellyfin config

    reverse_proxy /Users/ForgotPassword localhost:8096,
    reverse_proxy /Users/ForgotPassword/Pin localhost:8096 {
        header_up X-Forwarded-For <any local ip address>
    }

    reverse_proxy localhost:8096

}
```

I use nginx personally so don't have experience with other proxies like caddy or apache. Feel free to create an PR/Issue or contact me if you want to add an example.
