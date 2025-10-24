#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PROJECT_ID="uber-clone-api-325213"
PROJECT_NUMBER="557303580741"
SERVICE_ACCOUNT_NAME="github-actions-terraform"
POOL_NAME="github-pool"
PROVIDER_NAME="github-provider"

echo -e "${GREEN}Setting up GitHub Actions CI/CD with Workload Identity Federation${NC}"
echo ""

# Prompt for GitHub repository
read -p "Enter your GitHub repository (format: owner/repo, e.g., johndoe/sre-platform): " GITHUB_REPO

if [ -z "$GITHUB_REPO" ]; then
  echo "Error: GitHub repository is required"
  exit 1
fi

echo ""
echo -e "${YELLOW}Step 1: Enabling required APIs...${NC}"
gcloud services enable iamcredentials.googleapis.com \
  cloudresourcemanager.googleapis.com \
  sts.googleapis.com \
  --project=$PROJECT_ID

echo ""
echo -e "${YELLOW}Step 2: Creating service account...${NC}"
if gcloud iam service-accounts describe ${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com --project=$PROJECT_ID &>/dev/null; then
  echo "Service account already exists, skipping creation"
else
  gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
    --display-name="GitHub Actions Terraform" \
    --description="Service account for GitHub Actions CI/CD" \
    --project=$PROJECT_ID
fi

echo ""
echo -e "${YELLOW}Step 3: Granting IAM permissions...${NC}"
for ROLE in "roles/run.admin" "roles/iam.serviceAccountUser" "roles/storage.admin" "roles/monitoring.admin" "roles/pubsub.admin" "roles/cloudfunctions.admin" "roles/artifactregistry.writer"; do
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="$ROLE" \
    --condition=None \
    --quiet
done

echo ""
echo -e "${YELLOW}Step 4: Creating Workload Identity Pool...${NC}"
if gcloud iam workload-identity-pools describe $POOL_NAME --location="global" --project=$PROJECT_ID &>/dev/null; then
  echo "Workload Identity Pool already exists, skipping creation"
else
  gcloud iam workload-identity-pools create $POOL_NAME \
    --location="global" \
    --display-name="GitHub Actions Pool" \
    --project=$PROJECT_ID
fi

echo ""
echo -e "${YELLOW}Step 5: Creating OIDC provider...${NC}"
if gcloud iam workload-identity-pools providers describe $PROVIDER_NAME --location="global" --workload-identity-pool=$POOL_NAME --project=$PROJECT_ID &>/dev/null; then
  echo "OIDC provider already exists, skipping creation"
else
  gcloud iam workload-identity-pools providers create-oidc $PROVIDER_NAME \
    --location="global" \
    --workload-identity-pool=$POOL_NAME \
    --display-name="GitHub Provider" \
    --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
    --attribute-condition="assertion.repository_owner == '${GITHUB_REPO%%/*}'" \
    --issuer-uri="https://token.actions.githubusercontent.com" \
    --project=$PROJECT_ID
fi

echo ""
echo -e "${YELLOW}Step 6: Binding service account to GitHub repository...${NC}"
gcloud iam service-accounts add-iam-policy-binding \
  ${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_NAME}/attribute.repository/${GITHUB_REPO}" \
  --project=$PROJECT_ID

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "=================================================="
echo "Add these secrets to your GitHub repository:"
echo "=================================================="
echo ""
echo "1. GCP_WORKLOAD_IDENTITY_PROVIDER"
echo "   projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_NAME}/providers/${PROVIDER_NAME}"
echo ""
echo "2. GCP_SERVICE_ACCOUNT"
echo "   ${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
echo ""
echo "=================================================="
echo ""
echo "Go to: https://github.com/${GITHUB_REPO}/settings/secrets/actions"
echo "And add the two secrets above."
