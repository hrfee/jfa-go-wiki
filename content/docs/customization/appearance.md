---
title: "Appearance"
date: 2021-06-23T17:30:30+01:00
draft: false
weight: 2
---

# Appearance

## CSS

jfa-go uses [Tailwind CSS](https://tailwindcss.com/) as a CSS processor/generator with the [a17t](https://a17t.miles.land) plugin. 2 color themes are supplied with jfa-go, "Default" \& "Jellyfin".
* `Default` is the default appearance of a17t, and is a light theme.
* `Jellyfin` is a passing attempt to recreate the Jellyfin look , and is a dark theme.

There is no easy facility for injecting custom CSS like Jellyfin has, so you'll just have to edit the `css/base.css` file directly. Colours can be more easily adjusted in the `css/dark.js` file (replacing the "Jellyfin" theme). To make any of these changes, you'll have to [compile the app yourself]({{< relref "/docs/dev/build" >}}).

Alternatively, you can source your own CSS files (or inline some) in the HTML files you supply using the method below, and that way you won't need to recompile each release yourself.

## HTML

One can specify a path to a folder containing customized HTML files with the `files/html_templates` setting. Any files that match the names of jfa-go's internal templates will be loaded instead. The files use go's built in templating language, so familiarize yourself with it first ([a good resource](https://blog.gopheracademy.com/advent-2017/using-go-templates/)) so you know what different parts do. You can find the internal templates [here](https://github.com/hrfee/jfa-go/tree/main/html), **HOWEVER**: These files are modified a bit during the build process, so they won't work straight from git! A fix is to compile the program, then take the files from there. See instructions [here](https://wiki.jfa-go.com/docs/build/binary/); build with `INTERNAL=off`, and valid HTML files will then be found in `build/data/html/`.

## Text/Translation

Additionally, All text on the page, including password requirement strings (e.g "Must have at least n characters") can be customized. The `files/lang_files` setting should be the path to a custom language directory that follows the same structure as the internal [lang](https://github.com/hrfee/jfa-go/tree/main/lang) directory:
```shell
lang/
├─ admin/
│  ├─ en-us.json
├─ form/
│  ├─ en-us.json
├─ pwreset/
│  ├─ en-us.json
├─ telegram/
│  ├─ en-us.json
├─ common/
│  ├─ en-us.json
├─ setup/
│  ├─ en-us.json
```
Copy one of the internal language files from `lang/<admin|form|pwreset|telegram|common|setup>` into it and change the name in the file, this will appear in settings. You can also provide a fallback language (anything you don't translate will fall back to this language).
```json
{
    "meta": {
        "name": "My custom lang"
        // "fallback": "sv-se"
    },
    "strings": {
    }
}
```

If you want to replace the internal language file, leave `name` the same. Restart jfa-go and you should see a new option in Settings > General > Language.

Good luck!
