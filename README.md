# Jamf-project - CI/CD Pipeline Demo

**Metacluster Systems Development Engineer II Homework** - Complete CI/CD pipeline for Flask "Hello World" app with GitHub Actions, Helm, and Argo CD GitOps.

[ [

## Features

- ✅ Flask "Hello world" app + pytest unit tests
- ✅ GitHub Actions CI: test → build → Trivy scan → Docker Hub push
- ✅ Helm chart with staging/prod environments
- ✅ Argo CD GitOps (auto-sync, self-healing)
- ✅ Local testing: Docker Desktop / Minikube
- ✅ Enterprise-ready: image scanning, multi-env, GitOps

## Quick Start (Local)

### 1. Run Flask app
```bash
cd app
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
flask --app app run --host=0.0.0.0 --port=5000
```
`curl http://localhost:5000` → **"Hello world"**

### 2. Run tests
```bash
cd app && pytest test_app.py -v
```
**All tests pass** ✓

### 3. Build Docker image
```bash
docker build -t jj1729/hello-world-flask:latest .
docker run -p 5000:5000 jj1729/hello-world-flask:latest
```

## Kubernetes Deployment

### Docker Desktop / Minikube
```bash
# Load image (Minikube)
minikube image load jj1729/hello-world-flask:latest

# Deploy Helm chart
kubectl create ns hello-staging || true
cd helm
helm upgrade --install hello-world . \
  --namespace hello-staging \
  --set image.repository=jj1729/hello-world-flask \
  --set image.tag=latest

# Access app
kubectl port-forward svc/hello-world 8080:80 -n hello-staging
curl http://localhost:8080  # "Hello world"
```

## CI/CD Pipelines

### CI (`ci.yaml`)
**Triggers**: `push`/`pull_request` to `main`

```
1. pytest app/test_app.py ✓
2. docker build → jj1729/hello-world-flask:${GITHUB_SHA}
3. Trivy vulnerability scan (CRITICAL/HIGH)
4. Push to Docker Hub
```

**Secrets needed**: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` (Read+Write)

### CD (`cd.yaml`) 
**Triggers**: `push main` (staging) + manual (staging/prod)

| Environment | Namespace | Replicas | Image Tag | Values File |
|-------------|-----------|----------|-----------|-------------|
| **Staging** | `hello-staging` | 1 | `${GITHUB_SHA}` | `values-staging.yaml` |
| **Production** | `hello-production` | 2 | `prod` | `values-prod.yaml` |

## GitOps with Argo CD

### Local Argo CD Setup
```bash
kubectl create ns argocd || true
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl port-forward svc/argocd-server -n argocd 8080:443
# UI: http://localhost:8080 (admin + base64-decoded secret)
```

### Argo CD Application
`argocd/hello-world-staging.yaml` watches `helm/` directory:
```
git push → CI builds image → Argo CD auto-syncs → Deployed
```

**Self-healing**: Manual `kubectl scale --replicas=0` → Argo CD restores ✓

## Repository Structure

```
├── app/                    # Flask app + tests
│   ├── app.py
│   ├── test_app.py
│   └── requirements.txt
├── helm/                   # Helm chart
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-staging.yaml
│   ├── values-prod.yaml
│   └── templates/
│       ├── deployment.yaml
│       └── service.yaml
├── .github/workflows/      # CI/CD
│   ├── ci.yaml
│   └── cd.yaml
├── argocd/                 # GitOps
│   └── hello-world-staging.yaml
├── Dockerfile
└── README.md
```

## Testing & Troubleshooting

### Common Issues Fixed

| Problem | Error | Solution |
|---------|-------|----------|
| **Docker push 401** | `insufficient scopes` | Docker Hub token → **Read+Write** |
| **Service not found** | `svc/hello-world-local` | `kubectl get svc` → `hello-world` (Helm template) |
| **Argo CD repo** | `Repository not found` | Make repo **public** or add GitHub token |
| **ImagePullBackOff** | Minikube | `minikube image load jj1729/hello-world-flask:latest` |
| **CD kubectl** | `localhost:8080 refused` | Local `helm upgrade` (no kubeconfig in GitHub runner) |

### Validation Steps
```bash
pytest app/test_app.py                    # Tests ✓
docker build -t test .                    # Docker ✓
helm lint helm/                           # Helm ✓
helm template helm/                       # Render ✓
curl localhost:8080                       # App ✓
```

## Homework Requirements [Metacluster PDF]

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Simple web app + "Hello world" | ✅ | `app.py` + `test_app.py` |
| GitHub CI workflow | ✅ | `ci.yaml` → [Actions](https://github.com/JJ8817/Jamf-project/actions) |
| Helm chart for K8s | ✅ | `helm/` → `kubectl get all -n hello-staging` |
| CD pipeline (local) | ✅ | `cd.yaml` + manual `helm upgrade` |
| Multi-environment | ✅ | `values-staging.yaml` vs `values-prod.yaml` |
| README for reproduction | ✅ | This file |

**Time spent**: ~8 hours (under 10hr limit)

## Demo Script (90min Interview)

```
[5m] "Complete pipeline: git → CI → Docker → Helm → Minikube"
[10m] Live: git push → CI green → helm upgrade → curl ✓
[10m] Argo CD UI: Synced/Healthy + self-healing demo
[15m] Staging vs Prod values + security scanning
[30m] Trade-offs + enterprise improvements
```

## Enterprise Improvements

- **Security**: Cosign signing, Trivy fail-on-critical, OIDC kubeconfig
- **Observability**: Prometheus/Grafana, app metrics endpoint
- **Reliability**: HorizontalPodAutoscaler, PDBs, multi-az
- **GitOps**: Argo Rollouts (blue-green/canary), image promotion policy

## Resources Used

- [Flask Quickstart](https://flask.palletsprojects.com)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices)
- [Argo CD Getting Started](https://argo-cd.readthedocs.io)
- [Trivy GitHub Action](https://github.com/aquasecurity/trivy-action)
- StackOverflow + GitHub docs for troubleshooting

***

**Status: Interview-ready!** 🚀 Push to main → demo live → "Hello world" = success.

Sources
