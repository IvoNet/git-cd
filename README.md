# gcd

`gcd` stands for git change directory.

The terminal is the most important tool in my tool-belt and as such I like to give it presents :-)
I am also a developer and change directories all the time in the terminal between git projects I'm working on.
This tool has made my life infinitely more pleasurable by having this awesome easy to use functionality!

When using it it will scan your home folder for all git projects and create a database based on it what it finds.

Now you can search for projects lightning fast and change to the directory.
It will keep statistics of the most chosen projects and if you run `gcd` without parameters it will show the top 10 list.

If it finds only one entry it will move into that folder, but if it finds more entries it will present a menu.

The more it gets used the better your top 10 will become. The tool is very flexible in how you want to use it.
In order to get the most out of it you should take the tome to read on :-)

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
| cdc         | `ccd` + exec command in that directory       | `cdc [alias]`                     |
| ccd-help    | show all aliases with their directories      | `ccd-help`                        |
| ccd-alias   | Set an alias to the active folder            | `ccd-alias <alias>`               |
| ccd-unalias | removes an alias                             | `ccd-unalias <alias>`             |
| cdi         | `gcd` + exec command in that directory       | `cdi ["regex"/word]`              |
| gcd-add     | Add the current folder                       | `gcd-add`                         |
| gcd-scan    | Rebuild the cache in the background          | `gcd-scan`                        |
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
| GCD_EXEC        | exec command after cdi/cdc (default `ls -lsa`)| `export GCD_EXEC="idea ."`        |
| CDC_EXEC        | exec command after cdc (default `$GCD_EXEC`)  | `export CDC_EXEC="idea ."`        |
| CDI_EXEC        | exec command after cdi (default `$GCD_EXEC`)  | `export CDI_EXEC="idea ."`        |
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

## Run a command after cd

The `cdi` command is a small extention on the `gcd` command.
It will run a command after it performed the change directory. This defaults to `ls -lsa` for showing 
the directory contents.

If you want to change this setting to e.g. IntelliJ or VS Code this is easily done.

### Intellij 

* add `export GCD_EXEC="idea ."` to your startup scripts (.zshrc / .bashrc / or equivalent). In order for this to work you need to have IntelliJ on your machine and the `Tools` > `Create Command-line launcher...` installed.
* refresh the terminal shells 
* try `cdi` command

### Visual Studio Code

* add `export GCD_EXEC="code ."` to your startup scripts (.zshrc / .bashrc / or equivalent)
* refresh the terminal shells 
* try `cdi` command



# Advanced

## gcd advanced aliases

Some examples of more advanced possible aliases

```bash
# Start with Visual Studo Code
alias ccdc='CDC_EXEC="code ." cdc'
alias cdic='CDI_EXEC="code ." cdi'

# list dir
alias cdcl='CDC_EXEC="ls -lsa" cdc'
alias cdil='CDI_EXEC="ls -lsa" cdi'
```

## Alias already exist?

Add this method to your .zshrc or equivalent and renew your shell.
When you run ccdg without anything it will see if you already have an alias for the folder you are standing in.
You can also provide an expression to look for.

```bash
ccdg() {
    if [[ -z "$1" ]]; then
        ccd-help | grep "$(pwd)"
        if [ $? -ne 0 ]; then
            echo "No alias found for this directory..."
        fi
    else
        ccd-help | grep "$1"
        if [ $? -ne 0 ]; then
                echo "No alias found for this query..."
        fi
    fi
}
```

e.g. `ccdg foo` will search for an alias or folder in the alias list that contains foo

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

# Uninstall

In order to completely uninstall git-cd you need to do the following:

* `brew uninstall git-cd`
* `rm -rfv ${HOME}/.gcd`

That's it.

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
