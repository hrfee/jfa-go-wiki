---
title: "TLS Setup"
date: 2021-06-23T17:44:41+01:00
draft: false
weight: 90
---

# TLS (HTTPS)

It's expected that you run jfa-go behind a reverse proxy with HTTPS. If you don't want to use one, you can set up TLS encryption directly in jfa-go. This also comes with the benefit of HTTP/2 support, which in some cases may slightly speed up load times.

TLS can be enabled in the `Advanced` section (if hidden, make sure to check `Show advanced settings`. You will need a certificate and key for this. You can get these from [Let's Encrypt](https://letsencrypt.org), or if using on a local network or placing behind a reverse proxy, you can generate them yourself with:

```shell
$ openssl genrsa -out server.key 2048 # Your key file, set the path to this in [advanced]/tls_key
$ openssl req -new -x509 -key server.key -out server.pem -days 365 # Your cert, set the path to this in [advanced]/tls_cert
```
When enabled, jfa-go runs on port 8057 by default, which you can change with `[advanced]/tls_port`.
