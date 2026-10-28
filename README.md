# order-service: a live CI/CD example

A tiny "order total" API (10% off carts above Rs 500) with a full CI/CD pipeline.

```
app/pricing.py                 business logic
app/main.py                    web API  (/health, /total?cart_value=600)
tests/                         unit + API tests
Dockerfile                     how the app is packaged
.github/workflows/ci-cd.yml    the pipeline
k8s/deployment.yaml            desired state for Kubernetes (GitOps)
```

## 1. Try it on your laptop (5 min)

```bash
pip install -r requirements.txt
pytest -v                       # 6 tests should pass
python -m app.main              # then open http://localhost:8080/total?cart_value=600
```

## 2. Make the pipeline live on GitHub (10 min, free)

1. Create a new **public** repo on github.com called `order-service` (no README).
2. Push this folder:
   ```bash
   git init && git add . && git commit -m "first commit"
   git branch -M main
   git remote add origin https://github.com/<your-username>/order-service.git
   git push -u origin main
   ```
3. Open the **Actions** tab. You'll see the `ci-cd` run:
   - **CI - lint and test** runs first.
   - **CD - build, publish, release** builds the Docker image, smoke-tests it,
     pushes it to ghcr.io, and commits the new image tag into `k8s/deployment.yaml`.
4. Check **Packages** on your profile: the image is there, tagged with the commit SHA.

## 3. Watch CI block a bad change

```bash
git checkout -b break-discount
# in app/pricing.py change  >  to  >=
git commit -am "oops" && git push -u origin break-discount
```
Open a pull request. The **CI** job goes red: `assert 450.0 == 500`.
The CD job never runs, so the bug can't reach production. Revert and push again: green.

## 4. (Optional) Add real CD with Argo CD on a local cluster

```bash
# needs Docker Desktop + kind + kubectl
kind create cluster
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl port-forward svc/argocd-server -n argocd 8443:443   # UI at https://localhost:8443
# login: admin / password from:
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```
In the Argo CD UI create an app: repo = your GitHub repo, path = `k8s`, namespace = `default`,
sync policy = automatic. From now on every merge to `main` updates the tag in
`k8s/deployment.yaml`, and Argo CD rolls the new version into the cluster on its own.
(Make the ghcr.io package public so the cluster can pull it.)
