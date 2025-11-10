# ACEest Fitness & Gym – DevOps CI/CD Project

This repository contains:
- Flask application versions under `app/` (`ACEest_Fitness.py` and `ACEest_Fitness-V*`).
- Original Tkinter code (from assignment bundle) under `app/original/` for reference.
- `Jenkinsfile` (under `jenkins/`) implementing CI/CD with tests, SonarQube, Docker image build/push, and Kubernetes deploy.
- `Dockerfile` with build-arg to select which app version to package.
- Kubernetes manifests under `k8s/` for Blue-Green, Canary, A/B Testing, Rolling Update, and (placeholder) Shadow deployment.
- Pytest tests in `tests/` that run against all Flask versions.
- SonarQube configuration (`sonar-project.properties`) and a placeholder report in `docs/sonarqube-report/`.

## Quick Start (Local)

```bash
pip install -r requirements.txt
python app/ACEest_Fitness.py  # runs v1.0 on http://localhost:5000
python app/ACEest_Fitness-V1.3.py  # runs v1.3
```

## Build a Docker image for a specific version

```bash
# Build version 1.3
docker build --build-arg APP_FILE=app/ACEest_Fitness-V1.3.py -t 2024tm93169/aceest-fitness-gym:1.3 .
```

## Kubernetes (Minikube)

Enable ingress in Minikube and apply manifests in `k8s/` for each strategy.
