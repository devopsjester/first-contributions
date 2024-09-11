import requests
from datetime import datetime


def get_first_commit(user, org, token):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Search for commits by the user in the organization, sorted by author date in ascending order
    search_url = f"https://api.github.com/search/commits?q=author:{user}+org:{org}&sort=author-date&order=asc"
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
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
    else:
        return f"Error: {response.status_code} - {response.text}"


def main():
    user = input("Enter the GitHub username: ")
    org = input("Enter the GitHub organization: ")
    token = input("Enter your GitHub token: ")
    result = get_first_commit(user, org, token)
    print(result)


if __name__ == "__main__":
    main()
