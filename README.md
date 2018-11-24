# GetForks

Simple Python tool to clone all forks of specified repo.

Downloads every fork into its own folder named after use who created the fork, all stored in current directory.

# Installation

GetForks works as command line utility and requires Python3 and `requests` library (install via `pip install requests`). 

Clone this repository to suitable place on your desktop and either run script through Python or use provided shell or batch scripts. Consider adding this folder to your PATH variable for ease of use.

# Usage

You can get help by running program without args or with `--help` option.

usage: `python getforks.py original-repo-url [github-username] [github-password]`

* For public repos, [github-username] [github-password] aren't required.
* For private ones, either provide both your username and password, use only username and wait for password prompt or create special access token as outlined here: https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/ and save it enviromental variable called GITHUB_TOKEN. This variable will be automatically read in case password isn't provided but username is.

* Format of original-repo-url can either be an URL (https://github.com/Cyn1que/GetForks), or just an URI in format of owner-name/repo-name (Cyn1que/GetForks).