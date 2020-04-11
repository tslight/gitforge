# GIT FORGE API CLIENTS

**W.I.P.** API clients for GitHub & GitLab.

Run commands or query api on all projects or groups of an authenticated GitLab
or GitHub user.

So far only GitLab & GitHub are supported and the commands - `sync` (clone a
repository, or pull from it if already cloned) or `status` (show the local status of
the repository).

**Coming soon** - A wider array of forges, commands and configuration...

## INSTALLATION

`pip install gitforge`

## CONFIGURATION

Add personal access tokens and desired destination directories to
`~/.config/gitforge/config`. These defaults can be overridden on the command
line with the `--token` and `--destination` arguments. See below for more
details.

### AUTHENTICATION

Generate a **GitHub** *Personal Access Token* [here](https://github.com/settings/tokens).

Generate a **GitLab** *Personal Access Token* [here](https://gitlab.com/profile/personal_access_tokens).

## OPTIONS

### GITHUB

``` text
usage: github [-h] [-C PATH] [-r REPO [REPO ...]] [-d DESTINATION]
                  [-t TOKEN] [-P SSH/HTTP] [-i] [-c GIT COMMAND] [-v]

Clone or pull repos

optional arguments:
  -h, --help            show this help message and exit
  -C PATH, --config PATH
                        path to azure configuration file
  -r REPO [REPO ...], --repos REPO [REPO ...]
                        github repo names
  -d DESTINATION, --destination DESTINATION
                        destination path
  -t TOKEN, --token TOKEN
                        github personal access token
  -P SSH/HTTP, --protocol SSH/HTTP
                        protocol to use - ssh or http
  -i, --interactive     choose repos interactively
  -c GIT COMMAND, --command GIT COMMAND
                        git command to run
  -v                    increase verbosity
```

### GITLAB

``` text
usage: gitlab [-h] [-C PATH] [-p PROJECT [PROJECT ...] | -g GROUP
                  [GROUP ...]] [-d DESTINATION] [-t TOKEN] [-P SSH/HTTP] [-i]
                  [-r GIT COMMAND] [-v]

Clone or pull repos

optional arguments:
  -h, --help            show this help message and exit
  -C PATH, --config PATH
                        path to azure configuration file
  -p PROJECT [PROJECT ...], --projects PROJECT [PROJECT ...]
                        gitlab project names
  -g GROUP [GROUP ...], --groups GROUP [GROUP ...]
                        gitlab group names
  -d DESTINATION, --destination DESTINATION
                        destination path
  -t TOKEN, --token TOKEN
                        gitlab personal access token
  -P SSH/HTTP, --protocol SSH/HTTP
                        protocol to use - ssh or http
  -i, --interactive     choose projects interactively
  -r GIT COMMAND, --run GIT COMMAND
                        git command to run
  -v                    increase verbosity
```
