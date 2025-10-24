# GitHub Actions CI/CD Setup Guide

## Overview
This guide sets up automated Terraform deployments using GitHub Actions with secure authentication via GCP Workload Identity Federation (no service account keys needed).

## Prerequisites
- GCP Project: `uber-clone-api-325213`
- GitHub repository created
- `gcloud` CLI authenticated with Owner/Editor permissions

## Step 1: Enable Required APIs
```bash
gcloud services enable iamcredentials.googleapis.com \
  cloudresourcemanager.googleapis.com \
  sts.googleapis.com
```

## Step 2: Create Service Account for CI/CD
```bash
# Create service account
gcloud iam service-accounts create github-actions-terraform \
  --display-name="GitHub Actions Terraform" \
  --description="Service account for GitHub Actions CI/CD"

# Grant necessary permissions
gcloud projects add-iam-policy-binding uber-clone-api-325213 \
  --member="serviceAccount:github-actions-terraform@uber-clone-api-325213.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding uber-clone-api-325213 \
  --member="serviceAccount:github-actions-terraform@uber-clone-api-325213.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding uber-clone-api-325213 \
  --member="serviceAccount:github-actions-terraform@uber-clone-api-325213.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding uber-clone-api-325213 \
  --member="serviceAccount:github-actions-terraform@uber-clone-api-325213.iam.gserviceaccount.com" \
  --role="roles/monitoring.admin"

gcloud projects add-iam-policy-binding uber-clone-api-325213 \
  --member="serviceAccount:github-actions-terraform@uber-clone-api-325213.iam.gserviceaccount.com" \
  --role="roles/pubsub.admin"

gcloud projects add-iam-policy-binding uber-clone-api-325213 \
  --member="serviceAccount:github-actions-terraform@uber-clone-api-325213.iam.gserviceaccount.com" \
  --role="roles/cloudfunctions.admin"

gcloud projects add-iam-policy-binding uber-clone-api-325213 \
  --member="serviceAccount:github-actions-terraform@uber-clone-api-325213.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"
```

## Step 3: Create Workload Identity Pool
```bash
# Create workload identity pool
gcloud iam workload-identity-pools create "github-pool" \
  --location="global" \
  --display-name="GitHub Actions Pool"

# Create workload identity provider (replace YOUR_GITHUB_ORG and YOUR_REPO)
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --display-name="GitHub Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --issuer-uri="https://token.actions.githubusercontent.com"

# Get the Workload Identity Provider resource name (save this for GitHub secrets)
gcloud iam workload-identity-pools providers describe "github-provider" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --format="value(name)"
```

**Output example:**
```
projects/557303580741/locations/global/workloadIdentityPools/github-pool/providers/github-provider
```

## Step 4: Allow GitHub to Impersonate Service Account
**Replace `YOUR_GITHUB_ORG/YOUR_REPO` with your actual repository (e.g., `johndoe/sre-platform`)**

```bash
# Allow GitHub Actions from your repository to impersonate the service account
gcloud iam service-accounts add-iam-policy-binding \
  github-actions-terraform@uber-clone-api-325213.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/557303580741/locations/global/workloadIdentityPools/github-pool/attribute.repository/YOUR_GITHUB_ORG/YOUR_REPO"
```

## Step 5: Configure GitHub Repository Secrets
Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Add these two secrets:

1. **GCP_WORKLOAD_IDENTITY_PROVIDER**
   ```
   projects/557303580741/locations/global/workloadIdentityPools/github-pool/providers/github-provider
   ```

2. **GCP_SERVICE_ACCOUNT**
   ```
   github-actions-terraform@uber-clone-api-325213.iam.gserviceaccount.com
   ```

## Step 6: Test the Workflow
```bash
# Commit and push changes
git add .github/workflows/terraform.yml
git commit -m "Add GitHub Actions CI/CD for Terraform"
git push origin main
```

The workflow will:
- ✅ Run `terraform fmt -check` on push
- ✅ Run `terraform validate` on push
- ✅ Run `terraform plan` on push
- ✅ Comment plan output on pull requests
- ✅ Run `terraform apply` automatically on push to main/master

## Troubleshooting

### Error: "Failed to authenticate to Google Cloud"
- Verify Workload Identity Provider name is correct
- Check service account email is correct
- Ensure GitHub repo path matches exactly (case-sensitive)

### Error: "Permission denied"
- Verify all IAM roles are granted to the service account
- Check service account has `roles/iam.workloadIdentityUser` binding

### Error: "Backend initialization failed"
- Ensure service account has `roles/storage.admin` on the tfstate bucket
- Verify GCS backend configuration in `terraform/main.tf`

## Security Notes
- ✅ No service account keys stored in GitHub
- ✅ Authentication via OIDC token exchange
- ✅ Limited to specific GitHub repository
- ✅ Terraform state encrypted in GCS with versioning
- ✅ IAM permissions follow principle of least privilege

## Manual Apply (if needed)
If you need to manually apply changes:
```bash
cd terraform
terraform init
terraform plan
terraform apply
```
