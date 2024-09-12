import requests

def get_first_commit(user, org, token):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Get all repositories in the organization
    repos_url = f'https://api.github.com/orgs/{org}/repos'
    repos = requests.get(repos_url, headers=headers).json()

    first_commit = None
    first_commit_date = None

    for repo in repos:
        repo_name = repo['name']
        # Get all branches in the repository
        branches_url = f'https://api.github.com/repos/{org}/{repo_name}/branches'
        branches = requests.get(branches_url, headers=headers).json()

        for branch in branches:
            branch_name = branch['name']
            # Get all commits by the user in the branch
            commits_url = f'https://api.github.com/repos/{org}/{repo_name}/commits?author={user}&sha={branch_name}'
            commits = requests.get(commits_url, headers=headers).json()

            for commit in commits:
                commit_date = commit['commit']['author']['date']
                if not first_commit or commit_date < first_commit_date:
                    first_commit = commit
                    first_commit_date = commit_date

    if first_commit:
        print(f"First commit by {user}:")
        print(f"Repo: {first_commit['repository']['full_name']}")
        print(f"Date: {first_commit_date}")
        print(f"Message: {first_commit['commit']['message']}")
        print(f"URL: {first_commit['html_url']}")
    else:
        print(f"No commits found for user {user} in organization {org}.")

# Usage
user = 'username'
org = 'organization'
token = 'your_github_token'
get_first_commit(user, org, token)