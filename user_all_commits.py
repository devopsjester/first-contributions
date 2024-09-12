import argparse
import os
from datetime import datetime
import sys
import requests


def get_first_commit(user, org, token):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Get all repositories in the organization
    repos_url = f"https://api.github.com/orgs/{org}/repos"
    repos = requests.get(repos_url, headers=headers).json()

    first_commit = None
    first_commit_date = None

    for repo in repos:
        repo_name = repo["name"]
        # Get all branches in the repository
        branches_url = f"https://api.github.com/repos/{org}/{repo_name}/branches"
        branches = requests.get(branches_url, headers=headers).json()

        for branch in branches:
            branch_name = branch["name"]
            # Get all commits by the user in the branch
            commits_url = f"https://api.github.com/repos/{org}/{repo_name}/commits?author={user}&sha={branch_name}"
            commits = requests.get(commits_url, headers=headers).json()

            for commit in commits:
                commit_date = commit["commit"]["author"]["date"]
                if not first_commit or commit_date < first_commit_date:
                    first_commit = commit
                    first_commit_date = commit_date
                    first_commit["repository"] = repo
                    first_commit["repository"]["full_name"] = f"{org}/{repo_name}"

    print_first_commit_details(first_commit, user, first_commit_date, org, token)


def get_user_details(user, token):
    user_url = f"https://api.github.com/users/{user}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    user_data = requests.get(user_url, headers=headers).json()
    return user_data["created_at"]


def print_first_commit_details(first_commit, user, first_commit_date, org, token):
    if first_commit:
        # Get user creation date
        user_creation_date = get_user_details(user, token)

        # Calculate the difference in days
        user_creation_date_obj = datetime.strptime(
            user_creation_date, "%Y-%m-%dT%H:%M:%SZ"
        )
        first_commit_date_obj = datetime.strptime(
            first_commit_date, "%Y-%m-%dT%H:%M:%SZ"
        )
        days_difference = (first_commit_date_obj - user_creation_date_obj).days

        # Format dates to MM/DD/YYYY
        user_creation_date_formatted = user_creation_date_obj.strftime("%m/%d/%Y")
        first_commit_date_formatted = first_commit_date_obj.strftime("%m/%d/%Y")

        print(
            f"{user} onboarded on {user_creation_date_formatted}, and committed for the first time {days_difference} days later, on {first_commit_date_formatted}."
        )
    else:
        print(f"No commits found for user {user} in organization {org}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get the first commit of a user in a GitHub organization."
    )
    parser.add_argument("--user", required=True, help="GitHub username")
    parser.add_argument("--org", required=True, help="GitHub organization")
    args = parser.parse_args()

    token = os.getenv("API_ACCESS_TOKEN")

    if not token:
        print("Error: API_ACCESS_TOKEN environment variable not set.")
        sys.exit(1)

    get_first_commit(args.user, args.org, token)
