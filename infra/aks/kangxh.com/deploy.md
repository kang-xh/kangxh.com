# Deploy kangxh.com 

export SA_KEY=u8q18+A3xmibZ3LIP
export SA_NAME=kangxhsasea

kubectl create ns web

az acr login --name kangxhacrsea
az acr import --name kangxhacrsea --source docker.io/kangxh/kangxh.com:latest --image kangxh.com:latest

kubectl create secret generic kangxhsasea-secret --from-literal=azurestorageaccountname=$SA_NAME --from-literal=azurestorageaccountkey=$SA_KEY

kubectl apply -f kangxh.com.yaml

