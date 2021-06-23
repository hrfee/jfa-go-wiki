---
title: "Build docker container"
date: 2021-06-23T17:30:30+01:00
draft: false
---

# Docker
For multiarch support, the provided `Dockerfile` uses Docker [buildx](https://github.com/docker/buildx), which means you can't just build it with your regular `docker build`. To use it, you need to enable experimental features in `/etc/docker/daemon.json` or `$HOME/.docker/config.json` or instead by setting the environment variable `DOCKER_CLI_EXPERIMENTAL=enabled` to temporarily enable it.
```shell
$ cat /etc/docker/daemon.json 
{
    "experimental": true
}
```
You should then be able to run `docker buildx` and get a help page. If not, see the [build instructions](https://github.com/docker/buildx#building) to manually install it.
To build and load the container, you can then run 
```shell
$ git clone https://github.com/hrfee/jfa-go.git
$ cd jfa-go/
$ docker buildx build -t hrfee/jfa-go:unstable --load .
```
