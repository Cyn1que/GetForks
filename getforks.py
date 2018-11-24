#!/usr/bin/env python

import subprocess
import requests
import sys
import os
import re

github_general_endpoint = 'https://api.github.com/repos/'
forks_endpoint = '/forks'
environment_token_var = 'GITHUB_TOKEN'


def get_repos_forks(repo_adress: str, authentication: (str, str)):
    repo_fork_core = re.sub(
        '(http)?(s)?(:\/\/)?(www.)?github.com/', '', repo_adress).rstrip('/')
    repo_fork_endpoint = github_general_endpoint + repo_fork_core + forks_endpoint
    print('Requesting data from: {}'.format(repo_fork_endpoint))
    r = requests.get(repo_fork_endpoint, auth=authentication)

    if (r.status_code == 404):
        print("Repo you've tried to use for fork search either doesn't exist or you can't access with auth you've provided: {}".format(authentication))
        exit()
    if (r.status_code == 401):
        print("""Your authentication was unsuccessful, please recheck your username and 
                password/token stored in {} environment variable.""".format(environment_token_var))
        exit()
    elif (r.status_code != 200):
        print("Unexpected error happened while trying to get list of forks from GitHub.")
        exit()
    else:
        return r.json()


def wrong_params():
    print_usage()


def print_usage():
    print('''usage: getforks.py original-repo-url [github-username] [github-password]

    For public repos, github auth isn't required.
    For private ones, either provide both your username and password, use only username and wait for password prompt
        or create special access token as outlined here: https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/
        and save it enviromental variable called {}, which is automatically read in case password isn't provided but username is.

    Format of <original-repo-url> can either be an URL, or just an URI in format of <owner-name>/<repo-name>'''.format(environment_token_var))


def get_original_repo() -> str:
    return sys.argv[1]


def get_github_basic_auth() -> (str, str):
    return (sys.argv[2], sys.argv[3])


def get_token_auth() -> (str, str):
    if (environment_token_var in os.environ):
        print('Using token stored in environment variable {} for authentication.'.format(
            environment_token_var))
        return (sys.argv[2], os.environ[environment_token_var])
    else:
        return None


def basic_auth_prompt() -> (str, str):
    password = input("No {} environment variable found, please provide your password: ".format(
        environment_token_var))
    return (sys.argv[2], password)


def clone_forks(forks: list):
    forks_cloning_data = [
        {'url': fork['clone_url'],
         'user': fork['owner']['login']
         }
        for fork in forks
    ]

    print('\ngit output:\n==============================================================================================\n')

    for fork in forks_cloning_data:
        clone_repo(fork['url'], fork['user'])


def clone_repo(repo_adress: str, owner_username: str):
    print('Cloning repository: {}'.format(repo_adress))
    process = subprocess.Popen(
        ['git', 'clone', repo_adress, owner_username], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    output = process.communicate()[0]


def handle_input():
    arg_count = len(sys.argv)
    auth = None

    if arg_count == 1 or (arg_count == 2 and sys.argv[1] == '--help'):
        print_usage()
        exit()

    if arg_count == 2:
        print('Running without authentication')
    elif arg_count == 4:
        auth = get_github_basic_auth()
    elif arg_count == 3:
        auth = get_token_auth()
        if auth is None:
            auth = basic_auth_prompt()
    else:
        wrong_params()
        exit()

    forks = get_repos_forks(get_original_repo(), auth)
    clone_forks(forks)


if __name__ == "__main__":
    handle_input()
