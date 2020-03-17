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

## Search by simple string

```bash
gcd ebook
```

## Rescan for git repos

run the following command to rescan for projects.

```bash
gcdrescan
```

## Reset the metrics

run the following command to reset all the metrics.

```bash
gcdreset
```

# Advanced

## Look at the metrics db

e.g.:

```bash
sqlite3 -readonly -quote ~/.gcd/gcd.sqlite "SELECT * FROM projects ORDER BY called DESC, project LIMIT 20"
```
