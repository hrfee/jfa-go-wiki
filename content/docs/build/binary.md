---
title: "Build binaries"
date: 2021-06-23T17:30:30+01:00
draft: false
---

# Building binaries
* Note: The build process doesn't really work on Windows, and I doubt there's a need for first class support. Your best bet is to build in WSL with either method below and the `GOOS=windows` environment variable set.

To build, you need to compile the typescript and go, and generate email templates and config files. The build scripts were mostly ripped out of jf-accounts, so you'll need similar dependencies:
```
required:
    git
    python >= 3.6
    go >= 1.16
    node.js and npm (for tsc/esbuild, a17t, mjml, remixicon, markdown parser & uncss)
optional:
    libappindicator3-dev or equivalent (if building with tray icon on linux)
    gcc-mingw-w64-x86-64 or equivalent (if cross-compiling for windows on linux/macOS)
    upx (to compress the executable)
```
The main dependencies of the program will be automatically downloaded on compilation and can be seen in [go.mod](https://github.com/hrfee/jfa-go/blob/main/go.mod).

## Makefile

```shell
$ git clone https://github.com/hrfee/jfa-go
$ cd jfa-go
$ make all # [DEBUG=on] [INTERNAL=off] [UPDATER=on/docker] [TRAY=on] [GOESBUILD=on] [RACE=on] [...]
$ ls build/
jfa-go
```
A Makefile is provided, which requires the `make` command. Simply clone the repository and run `make all` to grab all necessary dependencies for go/python/node, compile everything and place the executable and app data inside `build/`. You can optionally compress the executable by running `make compress` after.

* If you get an error from npm regarding esbuild, this is because a precompiled binary for your system's architecture isn't available on npm. run `make all GOESBUILD=on` instead to have it compiled instead.

* You can optionally provide the path/name of the `go` executable manually with `make all GOBINARY=<path to go>`.

* More build-time variables exist, which are explained on the [contributing page](/docs/build/dev).

## Goreleaser
[goreleaser](https://github.com/goreleaser/goreleaser) is used to publish the packages seen in the release section. The `scripts/version.sh` wrapper generates the version and provides it to goreleaser with an environment variable.

The executables will be placed in `dist/`.
* To generate executables for multiple platforms:
```shell
$ ./scripts/version.sh goreleaser build --snapshot --rm-dist
```

* To generate package archives that include `LICENSE` and `README.md`:
```shell
$ ./scripts/version.sh goreleaser --snapshot --skip-publish --rm-dist
```
