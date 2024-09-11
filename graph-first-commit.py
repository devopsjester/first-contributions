import requests
import json

# Set up your GitHub token and organization name
GITHUB_TOKEN = "your_github_token"
ORG = "your_organization_name"

# Define the headers for the API request
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
}

# Define the GraphQL query to get organization members
query_members = """
query($org: String!, $cursor: String) {
  organization(login: $org) {
    membersWithRole(first: 100, after: $cursor) {
      pageInfo {
        endCursor
        hasNextPage
      }
      nodes {
        login
        createdAt
      }
    }
  }
}
"""

# Define the GraphQL query to get the first commit date for a user
query_first_commit = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      commitContributionsByRepository(maxRepositories: 1) {
        contributions(first: 1, orderBy: {field: OCCURRED_AT, direction: ASC}) {
          nodes {
            occurredAt
          }
        }
      }
    }
  }
}
"""


def run_query(query, variables):
    response = requests.post(
        "https://api.github.com/graphql",
        headers=headers,
        json={"query": query, "variables": variables},
    )
    response.raise_for_status()
    return response.json()


def get_members(org):
    members = []
    cursor = None
    while True:
        variables = {"org": org, "cursor": cursor}
        result = run_query(query_members, variables)
        members.extend(result["data"]["organization"]["membersWithRole"]["nodes"])
        page_info = result["data"]["organization"]["membersWithRole"]["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        cursor = page_info["endCursor"]
    return members


def get_first_commit_date(login):
    variables = {"login": login}
    result = run_query(query_first_commit, variables)
    contributions = result["data"]["user"]["contributionsCollection"][
        "commitContributionsByRepository"
    ]
    if contributions and contributions[0]["contributions"]["nodes"]:
        return contributions[0]["contributions"]["nodes"][0]["occurredAt"]
    return None


def main():
    members = get_members(ORG)
    results = []
    for member in members:
        login = member["login"]
        joining_date = member["createdAt"]
        first_commit_date = get_first_commit_date(login)
        results.append(
            {
                "login": login,
                "joining_date": joining_date,
                "first_commit_date": first_commit_date,
            }
        )

    # Output the results
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
