# AKS deploy

## ACR

    1. create acr named kangxhacrsea
    2. IAM is configured by az aks create command. 

## AKS

    az extension add --name aks-preview
    az extension list

    # verify resource in core resource group: 
    az resource list --resource-group MSDN-RG-Kangxh-AKS -o table

    # Create aks Resource Group
    az group create --name MSDN-RG-Kangxh-AKS --location southeastasia

    # transfer docker image from docker.io/kangxh to kangxhacrsea
    az acr login --name kangxhacrsea
    az acr import --name kangxhacrsea --source docker.io/kangxh/kangxh.com:latest --image kangxh.com:latest

    # get dependent resource ID
    OMSID=$(az monitor log-analytics workspace show --resource-group MSDN-RG-Kangxh-Mgmt -n kangxhomssea --query id -o tsv)
    SUBNET=$(az network vnet subnet show --resource-group MSDN-RG-Kangxh-Core --vnet-name kangxhvnetsea --name aks --query id -o tsv)
    PIP=$(az network public-ip show --resource-group  MSDN-RG-Kangxh-AKS --name kangxhpipsea-aks --query id -o tsv)

    # Create AKS, --node-resource-group is not supported in China yet.
    
    az aks create --resource-group MSDN-RG-Kangxh-AKS \
        --name kangxhakssea \
        --ssh-key-value  /mnt/c/kangxh/AzureLabs/SSHKey/common/id_rsa.pub \
        --admin-username kangxh \
        --workspace-resource-id $OMSID \
        --enable-addons monitoring \
        --enable-managed-identity \
        --location southeastasia \
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
        --attach-acr kangxhacrsea

    # Add B4 node pool.
    az aks nodepool add \
        --resource-group MSDN-RG-Kangxh-AKS \
        --cluster-name kangxhakssea \
        --name b4pool \
        --node-vm-size Standard_B4ms \
        --labels sku=b4vm \
        --node-osdisk-size 30 \
        --node-count 1

    # remove B4 node pool.
    az aks nodepool delete --resource-group MSDN-RG-Kangxh-AKS  --cluster-name kangxhakssea --name b4pool

    # donwload kubectl credential
    az aks get-credentials --resource-group MSDN-RG-Kangxh-AKS  --name kangxhakssea

    # Update b2 & b4 node pool. b2 will run most of time to host web
    az aks nodepool update --cluster-name kangxhakssea \
                        --name b2pool \
                        --resource-group MSDN-RG-Kangxh-AKS  \
                        --max-count 3 \
                        --min-count 1 \
                        --mode System 

    # scale to min size to save cost.
    az aks nodepool scale --cluster-name kangxhakssea --resource-group MSDN-RG-Kangxh-AKS  --name b2pool --node-count 1

    # upgrade aks
    az aks get-upgrades --resource-group MSDN-RG-Kangxh-AKS  --name kangxhakssea 
    az aks upgrade --resource-group MSDN-RG-Kangxh-AKS  --name kangxhakssea --kubernetes-version 1.16.7

    # ensure the Mananged Identity has Contributor access to AKS and AKS Resources group.

## Internet access

    to reduce complexity, ingress controller is not used. 
    service exposed via public ip address.

## Deploy kangxh.com 

export SA_KEY=u8q18+A3xmibZ3LIP
export SA_NAME=kangxhsasea

kubectl create ns web

az acr login --name kangxhacrsea
az acr import --name kangxhacrsea --source docker.io/kangxh/kangxh.com:latest --image kangxh.com:latest

kubectl create secret generic kangxhsasea-secret --from-literal=azurestorageaccountname=$SA_NAME --from-literal=azurestorageaccountkey=$SA_KEY

kubectl apply -f kangxh.com.yaml