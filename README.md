# gcd

`gcd` stands for git change directory.

When using it it will scan your home folder for all git projects and create a database based on it what it finds.

Now you can search for projects lightning fast and change to the directory.
It will keep statistics of the most chosen projects and if you run `gcd` without parameters it will show the top 10 list.

If it finds only one entry it will move into that folder, but if it finds more entries it will present a menu.

# How to use / Install

* Clone this project in your home folder to `.gcd`

```bash
cd ~
git clone https://github.com/IvoNet/git-cd.git .gcd
```

* add the following aliasses to your .profile / .zshrc or other startup script

```bash
alias gcd="source \${HOME}/.gcd/bin/gcd"
alias cdi="source \${HOME}/.gcd/bin/cdi"
alias gcdr="echo \"Resetting: \$(rm -fv \${HOME}/.gcd/gcd.cache 2>/dev/null)\""
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
