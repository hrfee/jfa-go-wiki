---
title: "Build docker container"
date: 2021-06-23T17:30:30+01:00
draft: false
---

# Docker
To build and load the container, run 
```shell
$ git clone https://github.com/hrfee/jfa-go.git
$ cd jfa-go/
$ docker buildx build -t hrfee/jfa-go:unstable --load .
```
## BuildX note
For multiarch support, the provided `Dockerfile` uses Docker [buildx](https://github.com/docker/buildx). In the past, this feature was experimental and required enabling manually. It should now be included by default. If docker complains it has no "buildx", try updating or enabling experimental features in `/etc/docker/daemon.json` or `$HOME/.docker/config.json`, or instead by setting the environment variable `DOCKER_CLI_EXPERIMENTAL=enabled` to temporarily enable it.
```shell
$ cat /etc/docker/daemon.json 
{
    "experimental": true
}
```
If that doesn't work, see the [build instructions](https://github.com/docker/buildx#building) to manually install it.
