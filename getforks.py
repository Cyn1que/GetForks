import subprocess
import requests
import sys
import re

github_general_endpoint = 'https://api.github.com/repos/'
forks_endpoint = '/forks'

def get_repos_forks(repo_adress: str, authentication: (str, str)):
    repo_fork_core = re.sub('(http)?(s)?(:\/\/)?(www.)?github.com/', '', repo_adress).rstrip('/')
    repo_fork_endpoint = github_general_endpoint + repo_fork_core + forks_endpoint
    print('Requesting data from: {}'.format(repo_fork_endpoint))
    r = requests.get(repo_fork_endpoint, auth=authentication)
    if (r.status_code == 404):
        print("Repo you've tried to use for fork search either doesn't exist or you can't access with auth you've provided: {}".format(authentication))
        exit()
    else:
        return r.json()

def wrong_params():
    print('Usage is: getforks <original-repo> <github-username> <github-password>')

def get_original_repo() -> str:
    if (len(sys.argv) < 2):
        wrong_params()
        exit()
    else: 
        return sys.argv[1]

def get_github_auth() -> (str, str):
    if (len(sys.argv) < 4):
        print("Running without auth") 
        return None
    else:
        return (sys.argv[2], sys.argv[3])

def clone_forks(forks: list):
    forks_cloning_data = [ 
        {'url': fork['clone_url'],
         'user': fork['owner']['login']
        }
        for fork in forks 
    ]
    for fork in forks_cloning_data:
        clone_repo(fork['url'], fork['user'])

def clone_repo(repo_adress: str, owner_username: str):
    print('Cloning repository: {}'.format(repo_adress))
    process = subprocess.Popen(['git', 'clone', repo_adress, owner_username], stdout=subprocess.PIPE)
    output = process.communicate()[0]

if __name__ == "__main__":
    forks = get_repos_forks(get_original_repo(), get_github_auth())
    clone_forks(forks)
    