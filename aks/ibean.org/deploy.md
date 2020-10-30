# Deploy ibean.org

export SA_KEY=ABCDABCDABCDABCDABCDABCDABCD  
export SA_NAME=kangzianweb

az acr login --name kangxhacrsea
az acr import --name kangxhacrsea --source docker.io/kangxh/ibean.org --image ibean.org:latest

kubectl create secret generic kangzianweb-secret --from-literal=azurestorageaccountname=$SA_NAME --from-literal=azurestorageaccountkey=$SA_KEY -n web

kubectl apply -f ibean.org.yaml