# GitHub First Commit Scripts

This repository contains scripts to retrieve the first commit of users in a GitHub organization. There are two main scripts:

1. `graph_first_commit.py`: Uses the GitHub GraphQL API to fetch the first commit date of all members in a specified organization.
2. `rest_first_commit.py`: Uses the GitHub REST API to fetch the first commit of a specified user in a specified organization.

## Prerequisites

- Python 3.12 or higher
- A GitHub API token with the necessary permissions to access the organization's data
- The `requests` library (installable via `pip`)

## Setup

1. Clone the repository.
2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv myenv
    source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Scripts

### `graph_first_commit.py`

This script fetches the first commit date for all members of a specified GitHub organization using the GitHub GraphQL API.

#### Usage

```sh
python3 graph_first_commit.py <organization_name> [--output <output_file>]
```

#### Example
```
export API_ACCESS_TOKEN=your_github_token
python3 graph_first_commit.py my-org --output results.json
```

#### Arguments

- `<organization_name>`: The name of the GitHub organization.
- `--output <output_file>` (optional): The file to save the results. If not provided, results will be printed to the console.

### `rest_first_commit.py`
This script fetches the first commit of a specified user in a specified GitHub organization using the GitHub REST API.

#### Usage
```
python rest_first_commit.py --user <GitHub username> --org <GitHub organization>
```

#### Example
```
export API_ACCESS_TOKEN=your_github_token
python3 rest_first_commit.py --user john-doe --org my-org
```

#### Arguments

- `--user <GitHub username>`: The GitHub username.
- `--org <GitHub organization>`: The name of the GitHub organization.

### `user_all_commits.py`
This script fetches the first commit of a specified user in all branches (not just the default one), in a specified GitHub organization using the GitHub REST API.

#### Usage
```
python user_all_commits.py --user <GitHub username> --org <GitHub organization>
```

#### Example
```
export API_ACCESS_TOKEN=your_github_token
python3 user_all_commits.py --user john-doe --org my-org
```

#### Arguments

- `--user <GitHub username>`: The GitHub username.
- `--org <GitHub organization>`: The name of the GitHub organization.

### Environment Variables

-- `API_ACCESS_TOKEN`: Your GitHub API token. This must be set before running the scripts.

## License
This project is licensed under the MIT License.