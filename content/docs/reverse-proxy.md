---
title: "Reverse Proxying"
date: 2021-06-23T17:30:30+01:00 
draft: false
weight: 12
---

# Reverse Proxying

## General
Reverse proxying should be relatively easy.

General rules:
* If you're proxying to a subdomain, e.g `accounts.jellyf.in/`, a `proxy_pass` or equivalent is enough.
* Set "External jfa-go URL" in Settings > General to where the root of jfa-go will be. With default settings, this is where you access the admin page. It should be a full url, e.g. `https://accounts.jellyf.in` or `https://jellyf.in/jfa-go`.
  * If you've changed the admin page path in Settings > "URL Paths", **don't** include it in "External jfa-go URL".
* If you're proxying to a subfolder, set "Reverse proxy subfolder" to the subfolder, including the preceding "/", e.g. `/jfa-go`.
  * Proxying to a subfolder is only supported for versions > 0.2.2.
  * Versions > v0.3.0 should be proxied to `<jfa-go address>/<your subfolder>`.
  * If you're placing jfa-go under the same subdomain as Jellyfin, make sure no CSP header is set for jfa-go's subfolder (see example below for NGINX).
* If you're proxying to multiple URLs (e.g. having one on your own, admin-facing domain and one on a user-facing domain), and you want URLs from the web app (such as invite links) to use the same URL you're accessing the page from, enable "Use reverse-proxy reported "Host" when possible". **Make sure your reverse proxy sets the "Host" and "X-Forwarded-Proto" headers**.
* If you choose to use jfa-go's IP logging, you'll need to make sure the proxy passes in the correct IP.
  * `X-Real-IP` or `X-Forwarded-For` will work.
  * The nginx and IIS examples includes at least one of these headers. You'll have to figure it out yourself for other proxies.
* **Cloudflare Users**: Make sure "Strong ETag headers" are respected. [This Cloudflare article](https://developers.cloudflare.com/cache/reference/etag-headers/#strong-etags) describes how. If you do not, parts of the page may load older version and mess things up in really irritating ways.


## Examples
Below are some simple examples of reverse proxy configs.

### NGINX (Subdomain)
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

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $http_host;
        proxy_buffering off;
    }
}
```

### NGINX (Subfolder on `/accounts` Jellyfin subdomain)

As mentioned, make sure to set "External jfa-go URL" to `https://jellyfin.your.domain/accounts`, and "Reverse Proxy subfolder" to `/accounts`.
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

    location ^~ /accounts {
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
        proxy_set_header X-Forwarded-Host $http_host;
        proxy_buffering off;
    }
}
```

### Traefik (`/jfa` subfolder)
Taken from [#53](https://github.com/hrfee/jfa-go/issues/53).
I'm not sure if this will include the X-Forwarded* headers, if you know/know a fix let me know.
```yaml
  jfa-go:
    # rest of your config
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.jfa-go.rule=Host(`services.${DOMAIN}`) && PathPrefix(`/jfa`)"
      - "traefik.http.routers.jfa-go.tls=true"
```

### IIS (`/accounts` subfolder)
From [#324](https://github.com/hrfee/jfa-go/discussions/324), credit to [kimboslice99](https://github.com/kimboslice99).
This config is for the `/accounts` subfolder. To change, adjust the `<action type="Rewrite"...` line near the bottom to
`<action type="Rewrite" url="http://localhost:8056/insert_subfolder_path_here/{R:1}" />`


```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
config requires URL Rewrite and Application Request Routing + run these commands from an elevated PowerShell 5.1 prompt
Set-WebConfigurationProperty -pspath 'MACHINE/WEBROOT/APPHOST'  -filter "system.webServer/proxy" -name "preserveHostHeader" -value "True"
Add-WebConfigurationProperty -pspath 'MACHINE/WEBROOT/APPHOST'  -filter "system.webServer/rewrite/allowedServerVariables" -name "." -value @{name='HTTP_X_FORWARDED_PROTOCOL'}
Add-WebConfigurationProperty -pspath 'MACHINE/WEBROOT/APPHOST'  -filter "system.webServer/rewrite/allowedServerVariables" -name "." -value @{name='HTTP_X_FORWARDED_PROTO'}
Add-WebConfigurationProperty -pspath 'MACHINE/WEBROOT/APPHOST'  -filter "system.webServer/rewrite/allowedServerVariables" -name "." -value @{name='HTTP_X_REAL_IP'}
Add-WebConfigurationProperty -pspath 'MACHINE/WEBROOT/APPHOST'  -filter "system.webServer/rewrite/allowedServerVariables" -name "." -value @{name='HTTP_X_FORWARDED_HOST'}
Add-WebConfigurationProperty -pspath 'MACHINE/WEBROOT/APPHOST'  -filter "system.webServer/rewrite/allowedServerVariables" -name "." -value @{name='HTTP_X_FORWARDED_PORT'}
-->
<configuration>
	<system.webServer>
        <rewrite>
            <rules>
            <clear />
                <rule name="Redirect to https" stopProcessing="true">
                    <match url=".*" />
                    <conditions logicalGrouping="MatchAny" trackAllCaptures="false">
                        <add input="{HTTPS}" pattern="off" />
                    </conditions>
                    <action type="Redirect" url="https://{HTTP_HOST}{REQUEST_URI}" redirectType="Found" />
                </rule><!-- These rules add X-Forwarded-Protocol -->
                <rule name="ForwardedHttps">
                    <match url=".*" />
                    <conditions logicalGrouping="MatchAll" trackAllCaptures="false">
                        <add input="{HTTPS}" pattern="On" />
                    </conditions>
                    <serverVariables>
                        <set name="HTTP_X_FORWARDED_PROTOCOL" value="https" />
                        <set name="HTTP_X_FORWARDED_PROTO" value="https" />
                    </serverVariables>
                </rule>
                <rule name="ForwardedHttp">
                    <match url=".*" />
                    <conditions logicalGrouping="MatchAll" trackAllCaptures="false">
                        <add input="{HTTPS}" pattern="Off" />
                    </conditions>
                    <serverVariables>
                        <set name="HTTP_X_FORWARDED_PROTOCOL" value="http" />
                        <set name="HTTP_X_FORWARDED_PROTO" value="http" />
                    </serverVariables>
                </rule>
                <rule name="jellyfinaccounts">
                    <match url="(.*)" />
                    <serverVariables>
                        <set name="HTTP_X_FORWARDED_HOST" value="{HTTP_HOST}" />
                        <set name="HTTP_X_REAL_IP" value="{REMOTE_ADDR}" />
                    </serverVariables>
                    <action type="Rewrite" url="http://localhost:8056/accounts/{R:1}" />
                </rule>
            </rules>
        </rewrite>
    </system.webServer>
</configuration>
```
