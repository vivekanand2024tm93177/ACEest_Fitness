# Setup Guide

## Prerequisites
- Docker, kubectl, Minikube
- Jenkins with Docker Pipeline + SonarQube plugins
- SonarQube server (local or remote)

## Jenkins Credentials (create)
- ID `dockerhub-creds` for Docker Hub
- SonarQube server named `My SonarQube Server` in Jenkins

## GitHub Repo Push (manual, secure)
```bash
git init
git add .
git commit -m "Initial commit - ACEest Fitness & Gym DevOps project"
git branch -M main
# Avoid pasting tokens into terminal history if possible.
export GITHUB_USER=2024TM93169
export GITHUB_TOKEN=YOUR_PAT_TOKEN_HERE
git remote add origin https://$GITHUB_USER:$GITHUB_TOKEN@github.com/2024tm93169/ACEest-Fitness-Gym-assignment2.git
git push -u origin main
```
