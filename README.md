# gcd

`gcd` stands for git change directory.

When using it it will scan your home folder for all git projects and create a database based on it
Now you can search for projects lightning fast and change to the directory

# how to use

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
