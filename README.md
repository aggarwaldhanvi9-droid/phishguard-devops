# PhishGuard — DevOps CI/CD & Kubernetes ML Microservice

**PhishGuard** is a real-time Phishing URL Detection REST API built with **FastAPI** and a **Scikit-Learn Random Forest** classifier.

## Pipeline Overview
- **CI (Git + GitHub + Jenkins):** Feature-branch workflow merged via Pull Request, declarative `Jenkinsfile` with SCM polling, automated `pytest` verification, and `.whl`/`.tar.gz` artifact packaging via `pyproject.toml`.
- **CD (Docker + Ansible + Kubernetes):** Containerized with `python:3.14-slim`, automated via an Ansible role/variables/handler playbook (`ansible/deploy.yml`), and orchestrated on Kubernetes (`ConfigMap`, 2-replica `Deployment` with `/health` `readinessProbe`, and `NodePort` `Service`).

## Quick Start
```bash
# Run tests & local API
pytest -v
uvicorn app.main:app --reload

# Deploy to Kubernetes via Ansible
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml
kubectl get all