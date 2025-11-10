#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/2024tm93169/ACEest-Fitness-Gym-assignment2.git"
DEFAULT_BRANCH="main"

if [[ -z "${GITHUB_USER:-}" || -z "${GITHUB_TOKEN:-}" ]]; then
  echo "Please export GITHUB_USER and GITHUB_TOKEN before running this script."
  echo "Example:"
  echo "  export GITHUB_USER=2024TM93169"
  echo "  export GITHUB_TOKEN=$MY_GITHUB_TOKEN"
  exit 1
fi

git init
git add .
git commit -m "Initial commit - ACEest Fitness & Gym DevOps project"
git branch -M "$DEFAULT_BRANCH"
git remote add origin "https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/2024tm93169/ACEest-Fitness-Gym-assignment2.git"
git push -u origin "$DEFAULT_BRANCH"
