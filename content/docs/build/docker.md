---
title: "Build docker container"
date: 2021-06-23T17:30:30+01:00
draft: false
---

# Docker
As mentioned in the [Binary section](/docs/build/binary), a prerequisite container is used to build jfa-go by the CI. This is also used in the supplied `Dockerfile`. Ths image is currently only published for `arm64`. You're probably using `amd64`, so you'll need to build the image yourself:

```
# git clone https://github.com/hrfee/jfa-go-build-docker.git
# cd jfa-go-build-docker
# docker buildx build -t docker.io/hrfee/jfa-go-build-docker:latest .
```

Now, somewhere else, build the actual project similarly:

```
# git clone https://github.com/hrfee/jfa-go.git
# cd jfa-go/
# docker buildx build -t hrfee/jfa-go:unstable .
```

## BuildKit note
For better multi-arch support, the main and prerequisite Dockerfiles take advantage of [BuildKit](https://docs.docker.com/build/buildkit/), the image builder included with Docker as of 23.0. It should also be included with Podman. You may have to install BuildKit/BuildX manually if you have an older version. 
