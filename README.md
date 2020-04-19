# GIT FORGE API CLIENTS

**W.I.P.** API clients for GitHub & GitLab.

## INSTALLATION

`pip install gitforge`

## CONFIGURATION

On first run you will be asked to enter a destination directory to sync to or
check the status of. You will also be asked to enter your Personal Access
Token.

Generate a **GitHub** *Personal Access Token* [here](https://github.com/settings/tokens).

Generate a **GitLab** *Personal Access Token* [here](https://gitlab.com/profile/personal_access_tokens).

These details will be stored in `$HOME/.gitforge.cfg`. You can edit this file
if you want to change the default destination directory or your access token.

The configuration looks something like this:

``` ini
[GitHub]
destination = /path/to/directory/to/store/repos
token = GITHUB-PERSONAL-ACCESS-TOKEN

[GitLab]
destination = /path/to/directory/to/store/repos
token = GITLAB-PERSONAL-ACCESS-TOKEN
```

These defaults can be overridden on the command line with the `--token` and
`--destination` arguments. See below for more details.

## COMMANDS

`sync`: Clone repositories *(and groups in the case of GitLab)* to
destination. If they already exist in destination - update them to the latest
remote commit. This is the default behaviour if no command is specified.

`status`: Check repositories in destination for uncommitted changes.

`jobs`: **GitLab ONLY** View the log of the last failed CI job run in
repository. This will be opened in a Curses paging window.

`schedules`: **GitLab ONLY** View all CI pipeline schedules ordered by next run
time.

`members`: **GitLab ONLY** View all members of groups or projects and their
access level.

**N.B.** If no repositories or groups are specified with `-r` or `-g`, then run
command against all of them... This may take a while depending on how many
repositories you have in your account.

## OPTIONS

### GITHUB

``` text
usage: gh [-h] [-d DESTINATION] [-i] [-p {ssh,http}] [-r REPOS [REPOS ...]]
          [-t TOKEN] [-v]
          [{sync,status,jobs,schedules}]

CLI GitHub API Client

positional arguments:
  {sync,status}
                        command to run (default: sync)

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
usage: gl [-h] [-d DESTINATION] [-i] [-p {ssh,http}] [-r REPOS [REPOS ...]]
          [-t TOKEN] [-v] [-g GROUPS [GROUPS ...]]
          [{sync,status,jobs,schedules}]

CLI GitLab API Client

positional arguments:
  {sync,status,jobs,schedules,members}
                        command to run (default: sync)

optional arguments:
  -d DESTINATION, --destination DESTINATION
                        destination path (default: None)
  -g GROUPS [GROUPS ...], --groups GROUPS [GROUPS ...]
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

## EXAMPLES

With all of these examples if you want more output or a better understanding of
what's going on use the `-v` argument.

**Clone or pull all repositories that you are a member of in the directory set
up in your configuration file**

`gitlab` for GitLab

`github` for GitHub

**N.B.** If you have not set up a configuration file or run the command before
you will be prompted for the destination directory and your Personal Access Token.

**Do the same as above but to an alternative directory, and use HTTP instead of
SSH**

`gitlab -d ~/path/to/alternative/directory -p http`

`github -d ~/path/to/alternative/directory -p http`

**Limit this action to only the "Example-Groups" and the "Example-Repos"**

`gitlab -d ~/path/to/alternative/directory -g Example-Group-1 Example-Group-2
Example-Repo-1 Example-Repo-2`

**N.B.** The group argument only works with GitLab. Also, all child groups will
be included when specifiying a parent group.

**Choose from a TUI menu the repositories you want to work with from the "Example-Group"**

`gitlab -g example-group -i`

You will be presented with a TUI menu which you can use the arrow keys to
navigate and the space bar to select repositories from.

**View the status of all the repositories in the directory set up in your
configuration**

`gitlab status` for GitLab

`github status` for GitHub

**View job logs of latest failed GitLab CI job from "project-1" & "project-2"
repository in a pager**

`gitlab jobs -r project-1 project-2`

**View CI pipeline schedules of all projects in "group-name" group**

`gitlab schedules -g group-name`

**View all members of "group-name" and "project-name"**

`gitlab members -g group-name -r project-name`
