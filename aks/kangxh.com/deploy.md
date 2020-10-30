# Deploy kangxh.com 

export SA_KEY=ABCDABCDABCDABCDABCDABCDABCDABCD
export SA_NAME=kangxhsaseaweb

kubectl create ns web

az acr login --name kangxhacrsea
az acr import --name kangxhacrsea --source docker.io/kangxh/kangxh.com:latest --image kangxh.com:latest

kubectl create secret generic kangxhsaseaweb-secret --from-literal=azurestorageaccountname=$SA_NAME --from-literal=azurestorageaccountkey=$SA_KEY -n web

