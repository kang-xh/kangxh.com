# Resource Deployment

## Core INfra

    - AKS as core infrastructure for workload host
    - VM only used for learning and management

### resource management with SPN

    cd /mnt/c/kangxh/AzureLabs/Certs/
    az cloud set --name AzureCloud
    az login --service-principal -u f9ac5c9b-9565-4983-a360-7d623432fd34 -p ./az-cli-spn-allenk-2037.pem --tenant microsoft.onmicrosoft.com

### Deploy AKS

####



## setup environment

    az configure --default group=MSFT-RG-Kangxh-Core
    az configure --default location=eastasia

## create aks


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

    # remove B4 node pool.
    az aks nodepool delete --resource-group MSFT-RG-Kangxh-AKS  --cluster-name kangxhaksea --name b4pool

    # donwload kubectl credential
    az aks get-credentials --resource-group MSFT-RG-Kangxh-AKS  --name kangxhaksea

    # Update b2 & b4 node pool. b2 will run most of time to host web
    az aks nodepool update --cluster-name kangxhaksea \
                        --name b2pool \
                        --resource-group MSFT-RG-Kangxh-AKS  \
                        --max-count 3 \
                        --min-count 1 \
                        --mode System 

    # scale to min size to save cost.
    az aks nodepool scale --cluster-name kangxhaksea --resource-group MSFT-RG-Kangxh-AKS  --name b2pool --node-count 1

    # upgrade aks
    az aks get-upgrades --resource-group MSFT-RG-Kangxh-AKS  --name kangxhaksea 
    az aks upgrade --resource-group MSFT-RG-Kangxh-AKS  --name kangxhaksea --kubernetes-version 1.16.7

    # ensure the Mananged Identity has Contributor access to AKS and AKS Resources group.



    # Deploy ibean.org

export SA_KEY=ABCDABCDABCDABCDABCDABCDABCD  
export SA_NAME=kangxhsaseaweb

az acr login --name kangxhacrsea
az acr import --name kangxhacrsea --source docker.io/kangxh/ibean.org --image ibean.org:latest

kubectl create secret generic kangxhsasea-secret --from-literal=azurestorageaccountname=$SA_NAME --from-literal=azurestorageaccountkey=$SA_KEY -n web

kubectl apply -f ibean.org.yaml

 # jenkins storage  

    use file share as jenkins storage. as the default access level is 0755, create PV to change it to 0777  

    kubectl apply -f jenkins.yaml  

# Jenkins Admin  

    kubectl exec jenkins-5787bd657f-8hrr9 -- cat /var/jenkins_home/secrets/initialAdminPassword
