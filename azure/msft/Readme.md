# Resource Deployment

## Core INfra

    - AKS as core infrastructure for workload host
    - VM only used for learning and management

### Resource management with SPN

    az cloud set --name AzureCloud
    az login --service-principal -u 784f9901-27e9-4a2c-9225-b94112269b0d -p ./az-cli-spn-allenk-2037.pem --tenant microsoft.onmicrosoft.com

### Deploy AKS

    az configure --default location=eastasia

#### create aks

    az extension add --name aks-preview

    az acr create -n kangxhacrea -g MSFT-RG-Kangxh-AKS --sku basic
    az acr login --name kangxhacrea
    az acr import --name kangxhacrea --resource-group MSFT-RG-Kangxh-AKS --source docker.io/kangxh/kangxh.com:latest --image kangxh.com:latest

    # get dependent resource ID
    OMSID=$(az monitor log-analytics workspace show --resource-group MSFT-RG-Kangxh-Mgmt -n kangxhomsea --query id -o tsv)
    SUBNET=$(az network vnet subnet show --resource-group MSFT-RG-Kangxh-Core --vnet-name kangxhvnetea --name aks --query id -o tsv)
    PIP=$(az network public-ip show --resource-group  MSFT-RG-Kangxh-AKS --name kangxhpipea-aks --query id -o tsv)

    # Create AKS
    
    az aks create --resource-group MSFT-RG-Kangxh-AKS \
        --name kangxhaksea \
        --ssh-key-value  /mnt/c/kangxh/AzureLabs/SSHKey/common/id_rsa.pub \
        --admin-username kangxh \
        --workspace-resource-id $OMSID \
        --enable-addons monitoring \
        --enable-managed-identity \
        --node-resource-group MSFT-RG-Kangxh-AKS-Node \
        --vm-set-type VirtualMachineScaleSets  \
        --network-plugin azure \
        --vnet-subnet-id $SUBNET \
        --docker-bridge-address 172.17.0.1/16 \
        --service-cidr   192.168.0.0/24 \
        --dns-service-ip 192.168.0.10 \
        --load-balancer-outbound-ips $PIP \
        --nodepool-name b2pool \
        --node-vm-size Standard_B2s \
        --nodepool-labels sku=b2vm \
        --node-osdisk-size 30 \
        --node-count 1 \
        --attach-acr kangxhacrea

    # Add B4 node pool.
    az aks nodepool add \
        --resource-group MSFT-RG-Kangxh-AKS \
        --cluster-name kangxhaksea \
        --name b4pool \
        --node-vm-size Standard_B4ms \
        --labels sku=b4vm \
        --node-osdisk-size 30 \
        --node-count 1

    # donwload kubectl credential
    az aks get-credentials --resource-group MSFT-RG-Kangxh-AKS  --name kangxhaksea

#### deploy application to aks

    export SA_KEY=ABCDABCDABCDABCDABCDABCDABCD  
    export SA_NAME=kangxhsaea

    kubectl create secret generic kangxhsaea-secret --from-literal=azurestorageaccountname=$SA_NAME --from-literal=azurestorageaccountkey=$SA_KEY 

##### kangxh.com

    az acr login --name kangxhacrea

    az acr import --name kangxhacrsea --source docker.io/kangxh/kangxh.com --image ibean.org:latest
    kubectl apply -f ibean.org.yaml

##### ibean.org

    az acr login --name kangxhacrea

    az acr import --name kangxhacrea --resource-group MSFT-RG-Kangxh-AKS --source docker.io/kangzian/ibean.org --image ibean.org:latest 
    kubectl apply -f ibean.org.yaml

##### nginx

    kubectl create namespace app
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    
    helm install nginx-ingress ingress-nginx/ingress-nginx \
    --namespace app \
    --set controller.replicaCount=2 \
    --set controller.nodeSelector."beta\.kubernetes\.io/os"=linux \
    --set defaultBackend.nodeSelector."beta\.kubernetes\.io/os"=linux \
    --set controller.admissionWebhooks.patch.nodeSelector."beta\.kubernetes\.io/os"=linux

###### jenkins

    use file share as jenkins storage. as the default access level is 0755, create PV to change it to 0777  

    kubectl apply -f jenkins.account.yaml
    kubectl apply -f jenkins.pv.yaml
    kubectl apply -f jenkins.yaml
    kubectl exec jenkins-5787bd657f-8hrr9 -- cat /var/jenkins_home/secrets/initialAdminPassword

###### SQL2019

    kubectl create secret generic mssql --from-literal=SA_PASSWORD="defaultdbpassword"
    kubectl apply -f sqlpvc.yaml
    kubectl apply -f sql2019.yaml


