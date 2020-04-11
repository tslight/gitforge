# GIT FORGE API CLIENTS

**W.I.P.** API clients for GitHub & GitLab.

So far, only the commands - `sync` *(clone a repository, or pull from it, if it
is already cloned)* & `status` *(show the local status of the repository)* are
implemented..

**Coming soon** - A wider array of forges, commands and configuration...

## INSTALLATION

`pip install gitforge`

## CONFIGURATION

Add personal access tokens and desired destination directories to
`~/.config/gitforge/config`. This file will be automatically installed if
`gitforge` is installed via `pip`, you just need to edit to suit your needs.

``` ini
[github]
destination = ~/src/github
token = GITHUB-PERSONAL-ACCESS-TOKEN

[gitlab]
destination = ~/src/gitlab
token = GITLAB-PERSONAL-ACCESS-TOKEN
```

These defaults can be overridden on the command line with the `--token` and
`--destination` arguments. See below for more details.

### AUTHENTICATION

Generate a **GitHub** *Personal Access Token* [here](https://github.com/settings/tokens).

Generate a **GitLab** *Personal Access Token* [here](https://gitlab.com/profile/personal_access_tokens).

## OPTIONS

### GITHUB

``` text
usage: github [-h] [-d DESTINATION] [-i] [-p {ssh,http}]
              [-r REPOS [REPOS ...]] [-t TOKEN] [-v]
              [{sync,status}]

CLI GitHub API Client

positional arguments:
  {sync,status}         command to run (default: sync)

optional arguments:
  -d DESTINATION, --destination DESTINATION
                        destination path (default: None)
  -h, --help            show this help message and exit
  -i, --interactive     choose repos interactively (default: False)
  -p {ssh,http}, --protocol {ssh,http}
                        protocol to use (default: ssh)
  -r REPOS [REPOS ...], --repos REPOS [REPOS ...]
                        GitHub repo names (default: None)
  -t TOKEN, --token TOKEN
                        GitHub personal access token (default: None)
  -v, --verbosity       increase verbosity (default: 0)
```

### GITLAB

``` text
usage: gitlab [-h] [-d DESTINATION] [-i] [-p {ssh,http}]
              [-r REPOS [REPOS ...]] [-t TOKEN] [-v] [-g GROUP [GROUP ...]]
              [{sync,status}]

CLI GitLab API Client

positional arguments:
  {sync,status}         command to run (default: sync)

optional arguments:
  -d DESTINATION, --destination DESTINATION
                        destination path (default: None)
  -g GROUP [GROUP ...], --groups GROUP [GROUP ...]
                        gitlab group names (default: None)
  -h, --help            show this help message and exit
  -i, --interactive     choose repos interactively (default: False)
  -p {ssh,http}, --protocol {ssh,http}
                        protocol to use (default: ssh)
  -r REPOS [REPOS ...], --repos REPOS [REPOS ...]
                        GitLab repo names (default: None)
  -t TOKEN, --token TOKEN
                        GitLab personal access token (default: None)
  -v, --verbosity       increase verbosity (default: 0)
```
