FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY git_pull_repos.py .

RUN pip install requests

ENV GIT_TERMINAL_PROMPT=0
ENV BASE_DIR=/app/repos
ENV PULL_INTERVAL_MINUTES=10

RUN mkdir -p $BASE_DIR

CMD ["python", "git_pull_repos.py"]