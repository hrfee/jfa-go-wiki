---
title: "Binaries"
date: 2021-06-23T17:30:30+01:00
draft: false
weight: 1
---

# Building binaries

You should build jfa-go on Linux or macOS, or in WSL. You could probably get it to work in Windows otherwise but don't torture yourself. Set the envvar `GOOS=windows` to build windows binaries with the Makefile.

## Dependencies

Build dependencies are written in Javascript and Go, both of which are needed for compilation anyway. The list of all deps are as follows: 
```
required:
    make (probably provided by some build tools package you already have)
    git
    go >= 1.24 (sorry, I think some dependency requires this)
    node.js and npm (for tsc/esbuild, tailwind/a17t, mjml, remixicon, markdown parser & uncss)
optional:
    libayatana-appindicator(3) or equivalent (if building with tray icon [TRAY=on] on linux)
    libolm-dev or equivalent (if building with Matrix E2EE, disable with [E2EE=off])
    gcc-mingw-w64-x86-64 or equivalent (if cross-compiling for windows on linux/macOS)
    python (for development -only-, some rarely used helper scripts are written in this)
```

The main Go dependencies are downloaded when building, and can be seen in [go.mod](https://github.com/hrfee/jfa-go/blob/main/go.mod).

## Suggestion: Docker

If you're comfortable with containers you might prefer building using the jfa-go-build-docker image, which includes all dependencies as well as bits for cross-compiling. The Dockerfile is [available on GitHub](https://github.com/hrfee/jfa-go-build-docker), and a pre-built image is [available on Docker Hub](https://hub.docker.com/r/hrfee/jfa-go-build-docker), sadly only for arm64 (The architecture of my CI server).

## Makefile
```shell
$ git clone https://github.com/hrfee/jfa-go
$ cd jfa-go
$ npm i
$ make # [DEBUG=on] [INTERNAL=off] [UPDATER=on/docker] [TRAY=on] [E2EE=off] [GOESBUILD=on] [RACE=on] [...]
$ ls build/
jfa-go
```


A Makefile is provided, which requires the `make` command. Simply clone the repository and run `make npm` (or just `npm i`) to grab node.js dependencies, then `make` to compile everything and place the executable (and app data if `INTERNAL=off`) inside `build/`.

* If you get an error from npm regarding esbuild, this is because a precompiled binary for your system's architecture isn't available on npm. run `make` with `GOESBUILD=on` instead to have it compiled instead.

* If you get some kind of pkg-config error, you probably missed a dependency. Install what it tells you or try with `TRAY=off` or `E2EE=off` if you don't care about either feature.

* You can optionally provide the path/name of the `go` executable manually with `make GOBINARY=<path to go>`.

* This is a proper Makefile (unlike it used to be), so compilation steps should only be performed when changes occur.
  * `make precompile` will do everything but compile the executable, useful if you want to modify some stuff before it's embedded in the executable.

* More build-time envvars exist, which should be relatively clear in the Makefile itself. The most relevant ones are described in [Development](/docs/dev/#environment-variables).

## Goreleaser
[goreleaser](https://github.com/goreleaser/goreleaser) is used to build and publish the packages seen in the release section and on [dl.jfa-go.com](https://dl.jfa-go.com). It compiles for multiple architectures, and expects all cross-compilation dependencies are available (as in the [prerequisite docker image](https://github.com/hrfee/jfa-go-build-docker)). The `scripts/version.sh` wrapper generates build time environment variables (version, shortcommit, etc.) which goreleaser needs. It also pulls some environment variables itself, which are supplied by the CI. Internally, it uses the Makefile for everything but compilation, so *make* sure `make` is installed along with the [above deps](#dependencies).

The executables will be placed in `dist/`.
* To generate executables for multiple platforms:
```shell
$ ./scripts/version.sh goreleaser build --snapshot --clean
```

* To generate package archives (zips, apks, debs, rpms) that include `LICENSE` and `README.md`:
```shell
$ ./scripts/version.sh goreleaser --snapshot --skip=publish --clean
