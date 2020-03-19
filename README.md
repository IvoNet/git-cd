# gcd

`gcd` stands for git change directory.

When using it it will scan your home folder for all git projects and create a database based on it what it finds.

Now you can search for projects lightning fast and change to the directory.
It will keep statistics of the most chosen projects and if you run `gcd` without parameters it will show the top 10 list.

If it finds only one entry it will move into that folder, but if it finds more entries it will present a menu.

The `cdi` command is a small extention on the `gcd` command for developers like me. If you run that it will not only
move into the folder but also open IntelliJ in that folder. In order for this to work you need to have IntelliJ on your
machine and the `Tools` > `Create Command-line launcher...` installed.

# How to use / Install

With [Homebrew](https://brew.sh)

```bash
brew tap ivonet/cli
brew install git-cd
```

The follow the instructions given by the install

# Commands

| Command     | Description                                  | Syntax                            |
|:----------- |:---------------------------------------------|:----------------------------------|
| gcd         | git (global) change directory                | `gcd ["regex"/word]`              |
| ccd         | Change directory based on alias              | `ccd [alias]`                     |
| ccd-help    | show all aliases with their directories      | `ccd-help`                        |
| cdi         | gcd + open Intellij Idea in that directory   | `cdi ["regex"/word]`              |
| gcd-alias   | Set an alias to the active folder            | `gcd-alias <alias>`               |
| gcd-rescan  | Rebuild the cache in the background          | `gcd-rescan`                      |
| gcd-unalias | removes an alias                             | `gcd-unalias <alias>`             |
| gcd-zap     | Zaps all non existing directories from cache | `gcd-zap`                         |
| gcdcron     | optional cron job to rebuild the cache       |  -                                |


# Example commands

## search with regular expression

```bash
gcd "ebook/.*parser$" 
```

## do nothing

If no parameters were given it will present the top 10 list. 
If no top 10 is (yet) available it will present the first 10 projects sorted by name
If you want another amount to be shown you can add e.g. `export GCD_FAVORITES=20` to your 
.zshrc / .bashrc or equivalent

```bash
gcd
```

## Scan different base folder

The default scanned base folder is ${HOME}, but you can override this
by exporting the following key in your startup scripts (.zshrc / .bashrc / or equivalent)

```bash
export GCD_PROJECTS_DIR="<your directory here>"
```

# Advanced

## Look at the metrics db

e.g.:

```bash
sqlite3 -readonly -quote ~/.gcd/gcd.sqlite "SELECT * FROM projects ORDER BY called DESC, project LIMIT 20"
```

## Cron job for updating

You can let the tool update itself at interval.
Please type the following for more help:

```bash
brew info git-cd
```

## Dev bin dir

In order to test new functionality it can be handy do set the GCD_BIN dir to this projects bin dir.
in order to do that do the following:

* open a terminal in the this projects bin dir

```bash
export GCD_DEV_DIR="$(pwd)"
```

* That will enable dev for this terminal shell session

# License

    Copyright 2020 (c) Ivo Woltring

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
