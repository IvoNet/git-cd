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
| ccd-alias   | Set an alias to the active folder            | `ccd-alias <alias>`               |
| cdi         | gcd + open Intellij Idea in that directory   | `cdi ["regex"/word]`              |
| gcd-add     | Add the current folder                       | `gcd-add`                         |
| gcd-rescan  | Rebuild the cache in the background          | `gcd-rescan`                      |
| gcd-unalias | removes an alias                             | `gcd-unalias <alias>`             |
| gcd-zap     | Zaps all non existing directories from cache | `gcd-zap`                         |
| gcdcron     | optional cron job to rebuild the cache       |  -                                |


# Options

you can `export` these options in your shell startup script (e.g. .zshrc / .profile / .bashrc) to 
change the default behavior.
You can also export it manually to change a setting for the current active shell only.

| Option          | Description                                   | Syntax (examples)                 |
|:--------------- |:----------------------------------------------|:----------------------------------|
| GCD_FAVORITES   | determine the amount of favorites to show     | `export GCD_FAVORITES=20`         |
| GCD_PROJECTS_DIR| overrides the default ${HOME} dir to scan     | `export GCD_PROJECTS_DIR="/"`     |
| GCD_EXEC        | exec this command after cdi (default `idea .`)| `export GCD_EXEC="code ."`        |
| GCD_DEV_BIN     | change bin location for dev purposes          | `export GCD_DEV_BIN="$(pwd)"`     |
  


# Example commands

## search with regular expression

Any regex is allowed but note that you use quotes or escape the 'weird' characters.

```bash
gcd "ebook/.*parser$" 
```

## do nothing

If no parameters were given it will present the top 10 list.
The `GCD_FAVORITES` option is used for this command... 

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
See the following for some examples.

```bash
#  This example will update every 6 hours
0 */6 * * * /usr/local/opt/git-cd/libexec/bin/gcdcron
#  This one every morning at 8 am
0 8 * * * /usr/local/opt/git-cd/libexec/bin/gcdcron
#  This one every day at 7 / 12 / 15 / 20 hours
0 7,12,15,20 * * * /usr/local/opt/git-cd/libexec/bin/gcdcron
```

To create a cron job:

* `crontab -e`
* add a line like the one above
* save and exit
* done


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
