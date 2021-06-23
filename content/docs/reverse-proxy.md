---
title: "Reverse Proxying"
date: 2021-06-23T17:30:30+01:00 
draft: false
---

# Reverse Proxying

Reverse proxying should be really easy.
* If you're proxying to a subdomain, e.g `accounts.jellyf.in/`, a `proxy_pass` or equivalent is enough.
* Proxying to a subfolder is only supported for versions > 0.2.2.
  * Versions > v0.3.0 don't need the URL Base stripped, but should be proxied to `<jfa-go address>/<URL base>` instead.
  * **Make sure to set the URL base in Settings > General (`ui > url_base` in config.ini).**
  * If you're placing it under the same subdomain as Jellyfin, make sure no CSP header is set for jfa-go's subfolder (see example below for NGINX).
  * Versions <= v0.3.0 require the proxy to strip the URL base.

Below are some simple examples of reverse proxy configs.

## NGINX (Subdomain)
```nginx
server {
    listen 80;
    server_name accounts.your.domain;
    return 301 https://accounts.your.domain/;
}
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name accounts.your.domain;

    # put your SSL config here
    
    location / {
        proxy_pass http://localhost:8056; # change as you need
        http2_push_preload on; # Should make the page load quicker.
    }
}
```

## NGINX (Subfolder on `/accounts` Jellyfin subdomain)

Make sure to set your URL Base to `/accounts` in Settings > General.
credit to [IngwiePhoenix](https://github.com/IngwiePhoenix).
```nginx
server {
    listen 80;
    server_name jellyfin jellyfin.your.domain;
    return 301 https://jellyfin.your.domain/;
}
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name jellyfin.your.domain;

    # rest of your own config

    location ~ ^/accounts(.*)$ {
        # No longer necessary on versions after v0.3.0
        # rewrite ^/accounts/(.*) /$1 break;
        
        # Remove the CSP header set for Jellyfin
        proxy_hide_header Content-Security-Policy;
        add_header Content-Security-Policy "";
       
        proxy_pass http://localhost:8056/accounts; # Change as you need
        
        # For versions <= v0.3.0
        #proxy_pass http://localhost:8056; # Change as you need
        
        http2_push_preload on; 

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Protocol $scheme;
        proxy_set_header X-Forwarded-Host $http_host;
        proxy_buffering off;
    }
}
```

## Traefik (subfolder on `/jfa` subfolder)
Taken from [#53](https://github.com/hrfee/jfa-go/issues/53).
```yaml
  jfa-go:
    # rest of your config
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.jfa-go.rule=Host(`services.${DOMAIN}`) && PathPrefix(`/jfa`)"
      - "traefik.http.middlewares.jfa-go-strip.stripprefix.prefixes=/jfa"
      - "traefik.http.routers.jfa-go.tls=true"
      - "traefik.http.routers.jfa-go.middlewares=jfa-go-strip@docker"
```
