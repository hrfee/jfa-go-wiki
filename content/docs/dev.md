---
title: "Building/Contributing for developers"
date: 2021-07-25T00:33:36+01:00
draft: false
---
# Development notes

Some stuff you might find helpful if you're trying to add to jfa-go.

## Code
I use 4 spaces for indentation. Go should ideally be formatted with `goimports` and/or `gofmt`. I don't use a formatter on typescript, so don't worry about that.

Code in Go should ideally use `PascalCase` for exported values, and `camelCase` for non-exported, JSON for transferring data should use `snake_case`, and Typescript should use `camelCase`. Forgive me for my many inconsistencies in this, and feel free to fix them if you want.

Functions in Go that need to access `*appContext` should be generally be receivers, except when the behaviour could be seen as somewhat independent from it (`email.go` is the best example, its behaviour is broadly independent from the main app except from a couple config values).

Integrations which synchronize user data with Jellyfin/jfa-go should ideally implement the `ThirdPartyService` interface. New contact method daemons should implement the `ContactMethodLinker` interface, and the users the `ContactMethodUser` one.

## Compiling

The Makefile is broken up into sections which depend on each other. When calling `make`, steps are performed only if there have been changes (i.e. typescript compiled when *.ts is changed). A few things, like build scripts, do not have their changes tracked. If you changed one of these, you can run `make clean` first before `make` to ensure your changes are used.

Below is an outline of the steps performed, by the variable used to call them in the Makefile. The ones LIKE_THIS are variables which you can't do `make THIS_WITH`, the lowercase ones you can.

|Step|Purpose|
|----|-------|
|`all`|Same as just running `make`.|
|`precompile`|Does everything except compile the binary.|
|`CONFIG_DEFAULT`|Generates `config-default.ini` from `config-base.yaml`, with default values and comments.|
|`configuration`|Alias you can call to run the above.|
|`EMAIL_TARGET`|Transpiles [mjml](https://mjml.io/) email templates into HTML files|
|`TYPESCRIPT_TARGET`|Applies [&quot;dark-variant&quot;](#dark-mode-css) changes to typescript, and transpiles into ES6 Javascript through esbuild. When DEBUG=on, also copies typescript into build directory, and generates sourcemaps.|
|`SWAGGER_TARGET`|Generates a `swagger.json` API doc file, and puts it where it needs to go, with swaggo&#39;s [gin-swagger](https://github.com/swaggo/gin-swagger).|
|`VARIANTS_TARGET`|Applies [&quot;dark-variant&quot;](#dark-mode-css) changes to HTML, and puts it where it needs to be.|
|`CSS_FULLTARGET`|Copies icons and fonts, bundles CSS, and calls tailwind to strip the CSS down.|
|`INLINE_TARGET`|Inlines CSS and javascript into the &quot;crash.html&quot; page, so it can be dumped to disk on crash and render correctly.|
|`COPY_TARGET`|Copies general static data (crash page, images, systemd service, language files and license) into the build directory.|
|`GO_TARGET`|Downloads Go dependencies and builds the binary.|
|`compile`|Alias you can call for the above.|
|`compress`|Calls [upx](https://upx.github.io/) to compress the binary, if you really want.|
|`install`|Copies the build directory (with the binary) to $DESTDIR.|
|`clean`|Removes build files.|
|`npm`|Calls `npm install`.|

## Environment variables

This isn't everything, but most of what'll actually be useful:

|VALUE=options|Default Value|Purpose|
|-------------|-------------|-------|
|`DEBUG=on/off`|off|Includes typescript sourcemaps and validates typescript.|
|`INTERNAL=on/off`|on|Embeds assets (html, js, images, etc.) into executable.|
|`UPDATER=on/docker/off`|off|Enables the updater, which pings the CI setup for updates. `on` is used for binary releases, `docker` for docker images.|
|`TRAY=on/off`|off|Adds a system tray icon, with start/stop/run at login options. Requires `appindicator` dependency.|
|`E2EE=on/off`|on|Includes support for end-to-end encryption for the Matrix bot. Requires `libolm-dev` dependency.|
|`GOESBUILD=on/off`|off|Whether or not to build the `esbuild` dependency with Go, or to download it with `npm`.|
|`RACE=on/off`|off|Whether or not to add the Go race detector.|
|`GOBINARY=<path>`|n/a|Path to an alternate Go executable.|
|`VERSION=v<semver>`|n/a|Alternative version number, for testing updater.|
|`COMMIT=<short commit>`|n/a|Commit build was done from. Should be in short format. Used for updater.|
|`BUILDTIME=<unix timestamp>`|n/a|Timestamp at which build was done. Also used for updater.|
|`LDFLAGS=<ldflags>`|n/a|Additional &quot;go build -ldflags&quot;.|
|`TAGS=tags`|n/a|Additional Go tags to build with, allows including code optionally at build time.|
|`OS=<os>`|n/a|Unrelated to GOOS, when set to `windows`, passes `-H=windowsgui` which disables stdout (hence stopping a terminal from opening).|

## Web API

Static Web API docs can be accessed by clicking [Web API Docs](https://api.jfa-go.com) on the sidebar or here.

A live version of the swagger documentation is available by running jfa-go with the `-swagger` argument to make it available at `http://localhost:8056/swagger/index.html`. If you're introducing any new routes when working on the API, make sure to give them a proper description above the function (see other routes in `api.go` as well as the [swaggo](https://github.com/swaggo/swag) documentation), and to put it in the appropriate category and/or file (e.g. `api-discord.go` for a discord-only method). If a struct used as a parameter or return type needs explanation, put descriptions of each field as a comment next to it (see [models.go](https://github.com/hrfee/jfa-go/blob/main/models.go)).

## Dark mode CSS

Dark mode is achieved with the tailwind `dark:` prefix, with an alternate version a17t's default colours. For example `class="card ~neutral"` becomes `class="card ~neutral dark:~d_neutral"`. You can mix and match these (i.e. neutral in light mode, urge in dark mode), or omit the dark variant entirely (the preprocessor scripts `scripts/dark-variant.sh` and `scripts/missing-colors.js` find missing ones and add them). 

## Config

The configuration is defined in `config/config-base.yaml`, whose structure is defined in [`common/config.go`](https://github.com/hrfee/jfa-go/tree/main/common/config.go). `scripts/ini/main.go` is the script which generates a `.ini` file from this. The yaml is included with the program, so that it can be sent to the web UI, where things descriptions and dependencies are actually rendered.

On dependencies, `depends_true/false` take the `setting` or `section` value (not the `name`!) of a setting or section. These evaluate as true how you'd expect, i.e. the value is a non-empty string, non-zero number or a true bool. Sections can define dependencies on settings with the format `section|setting`, i.e. To make `smtp` dependent on an email `method` being set, you'd do:
```yaml
- section: smtp
  meta:
    name: SMTP (Email)
    description: SMTP connection settings.
    depends_true: email|method
```
