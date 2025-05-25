
# GitHub Repositories Auto Sync

![Python](https://img.shields.io/badge/python-3.10-blue)
![Docker](https://img.shields.io/badge/docker-supported-blue)
![License](https://img.shields.io/badge/license-MIT-green)

This project contains a Python script and a Docker container setup to automatically synchronize all your GitHub repositories locally. The script clones or pulls your GitHub repositories into a specified directory at regular intervals.

---

## Features

- Automatically fetches all repositories you have access to from GitHub using your personal access token.
- Clones repositories if not present locally, or pulls the latest changes if they already exist.
- Runs in a loop, updating your repos periodically based on a configurable interval.
- Easy to run as a Docker container, suitable for environments like QNAP Container Station.

---

## Requirements

- A valid GitHub Personal Access Token (PAT) with at least `repo` scope.
- Docker (optional, but recommended for containerized use).
- (If running locally) Python 3.10+ and `requests` library.

---

## Environment Variables

The behavior of the script and container is controlled by the following environment variables:

| Variable             | Description                                                | Default      |
|----------------------|------------------------------------------------------------|--------------|
| `GITHUB_TOKEN`       | **Required.** Your GitHub Personal Access Token (PAT).    | None (required) |
| `BASE_DIR`           | Directory where repositories are cloned/updated.          | `/app/repos` |
| `PULL_INTERVAL_MINUTES` | Interval in minutes between repository update cycles.      | `10`         |

---

## How It Works

1. The script fetches your GitHub repositories using the GitHub API and your personal token.
2. It checks if each repository already exists in the `BASE_DIR`.
3. If the repo exists, it runs `git pull` to update it.
4. If the repo does not exist, it clones it.
5. The process repeats every `PULL_INTERVAL_MINUTES`.

---

## Running Locally

1. Set the environment variables:
    ```bash
    export GITHUB_TOKEN="your_github_token_here"
    export BASE_DIR="/path/to/local/repos"
    export PULL_INTERVAL_MINUTES=15
    ```

2. Install dependencies:
    ```bash
    pip install requests
    ```

3. Run the script:
    ```bash
    python git_pull_repos.py
    ```

---

## Running with Docker

The included Dockerfile builds a lightweight image based on `python:3.10-slim` that includes `git` and the required Python packages.

### Build the Docker Image

```bash
docker build -t github-auto-sync .
```

### Run the Docker Container

Make sure to pass the required environment variables (`GITHUB_TOKEN`, optionally `BASE_DIR` and `PULL_INTERVAL_MINUTES`):

```bash
docker run -d \
  -e GITHUB_TOKEN="your_github_token_here" \
  -e BASE_DIR="/app/repos" \
  -e PULL_INTERVAL_MINUTES=10 \
  -v /path/on/host/repos:/app/repos \
  --name github-auto-sync \
  github-auto-sync
```

---

## Usage on QNAP Container Station

This container is well-suited for running on **QNAP Container Station**:

1. Build or pull the image on your QNAP NAS.
2. Create a container with the environment variables set in Container Station:
   - `GITHUB_TOKEN` (your GitHub PAT)
   - `BASE_DIR` (optional, defaults to `/app/repos`)
   - `PULL_INTERVAL_MINUTES` (optional, defaults to 10)
3. Map a persistent volume on your NAS to `/app/repos` inside the container to keep the cloned repositories persistent across container restarts.
4. Start the container. It will continuously sync your GitHub repos based on the set interval.

---

## Notes

- The script disables git terminal prompts by setting `GIT_TERMINAL_PROMPT=0`.
- Make sure your GitHub token has sufficient permissions to access all your repositories.
- The sync interval defaults to 10 minutes if not set or if an invalid value is provided.

---

## License

MIT License
