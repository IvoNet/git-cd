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

* Clone this project in your home folder to `.gcd`

```bash
cd ~
git clone https://github.com/IvoNet/git-cd.git .gcd
```

* add the following aliases to your `.profile` / `.zshrc` / `.bashrc` or other startup script

```bash
alias gcd="source \${HOME}/.gcd/bin/gcd"
alias cdi="source \${HOME}/.gcd/bin/cdi"
alias gcdreset="echo \"Resetting: \$(rm -fv \${HOME}/.gcd/gcd.cache 2>/dev/null)\""
```

* Start a new terminal session (shell)
* Try: `gcd gcd` (this can take a while the first time)


# Example commands

## search with regular expression

```bash
gcd "ebook/.*pdfparser$" 
```

## do nothing

If no parameters were given it will present the top 10 list. 
If no top 10 is (yet) available it will present the first 10 projects sorted by name

```bash
gcd
```

## Search by simple string

```bash
gcd ebook
```

## Reset the cache

run the following command and the next time you use gcd it will rescan everything again.

```bash
gcdreset
```

# Advanced usage

## Reset completely

```bash
cd ~/.gcd
rm -f gcd.cache gcd.sqlite
gcd
```

## Use `gcd.py` standalone

The gcd.py script in the bin folder does function standalone but is specifically written for the gcd function.
It maintains the statistics and re-generates the gcd.cache file with the new sorting.

just run `python3 ./gcd.py -h` to get specific help
