"""
This module provides functionality to retrieve the first commit of a user in a GitHub organization.

The script uses the GitHub API to search for commits by a specified user within a specified organization,
sorted by author date in ascending order. The first commit found is returned.

Usage:
    Set the API_ACCESS_TOKEN environment variable with your GitHub token.
    Run the script with the following command:
        python3 rest_first_commit.py --user <GitHub username> --org <GitHub organization>

Functions:
    get_first_commit(user, org, token): Retrieves the first commit of a user in a GitHub organization.
    main(): Parses command-line arguments and calls get_first_commit.
"""

import os
import argparse
import sys
import requests


def get_first_commit(user, org, token):
    """
    Get the first commit of a user in a GitHub organization.

    Args:
        user (str): GitHub username.
        org (str): GitHub organization.
        token (str): GitHub API token.

    Returns:
        dict or str: A dictionary containing the SHA, URL, and date of the first commit,
                     or an error message if no commits are found or an error occurs.
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.cloak-preview",
    }
    # Search for commits by the user in the organization, sorted by author date in ascending order
    search_url = f"https://api.github.com/search/commits?q=author:{user}+org:{org}&sort=author-date&order=asc"

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

    commits = response.json().get("items", [])
    if commits:
        first_commit = commits[0]
        commit_sha = first_commit["sha"]
        commit_url = first_commit["html_url"]
        commit_date = first_commit["commit"]["author"]["date"]
        return {
            "sha": commit_sha,
            "url": commit_url,
            "date": commit_date,
        }
    else:
        return "No commits found for this user in the organization."


def main():
    """
    Main function to parse command-line arguments and get the first commit of a user in a GitHub organization.
    """
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

    result = get_first_commit(args.user, args.org, token)
    print(result)


if __name__ == "__main__":
    main()
