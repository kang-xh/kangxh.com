# AKS deploy

## ACR

    1. create acr named kangxhacrmc
    2. IAM is configured by az aks create command. 

## AKS

    az extension add --name aks-preview
    az extension list

    # verify resource in core resource group: 
    az resource list --resource-group mc-rg-Kangxh-AKS -o table

    # Create aks Resource Group
    az group create --name mc-rg-Kangxh-AKS --location chinaeast2

    # transfer docker image from docker.io/kangxh to kangxhacrmc
    az acr login --name kangxhacrmc
    az acr import --name kangxhacrmc --source docker.io/kangxh/kangxh.com:latest --image kangxh.com:latest

    # get dependent resource ID
    OMSID=$(az monitor log-analytics workspace show --resource-group mc-rg-Kangxh-Mgmt -n kangxhomsmc --query id -o tsv)
    SUBNET=$(az network vnet subnet show --resource-group mc-rg-Kangxh-Core --vnet-name kangxhvnetmc --name aks --query id -o tsv)
    PIP=$(az network public-ip show --resource-group  mc-rg-Kangxh-AKS --name kangxhpipmc-aks --query id -o tsv)

    # Create AKS
    az aks create --resource-group mc-rg-Kangxh-AKS \
        --name kangxhaksmc \
        --ssh-key-value  /mnt/c/kangxh/AzureLabs/SSHKey/common/id_rsa.pub \
        --admin-username kangxh \
        --workspace-resource-id $OMSID \
        --enable-addons monitoring \
        --enable-managed-identity \
        --location chinaeast2 \
        --vm-set-type VirtualMachineScaleSets  \
        --network-plugin azure \
        --vnet-subnet-id $SUBNET \
        --docker-bridge-address 172.17.0.1/16 \
        --service-cidr   192.168.0.0/24 \
        --dns-service-ip 192.168.0.10 \
        --load-balancer-outbound-ips $PIP \
        --node-resource-group mc-rg-Kangxh-AKS-Node \
        --nodepool-name b2pool \
        --node-vm-size Standard_B2s \
        --nodepool-labels sku=b2vm \
        --node-osdisk-size 30 \
        --node-count 1 \
        --attach-acr kangxhacrmc

    # Add B4 node pool.
    az aks nodepool add \
        --resource-group mc-rg-Kangxh-AKS \
        --cluster-name kangxhaksmc \
        --name b4pool \
        --node-vm-size Standard_B4ms \
        --labels sku=b4vm \
        --node-osdisk-size 30 \
        --node-count 1

    # remove B4 node pool.
    az aks nodepool delete --resource-group mc-rg-Kangxh-AKS  --cluster-name kangxhaksmc --name b4pool

    # donwload kubectl credential
    az aks get-credentials --resource-group mc-rg-Kangxh-AKS  --name kangxhaksmc

    # Update b2 & b4 node pool. b2 will run most of time to host web
    az aks nodepool update --cluster-name kangxhaksmc \
                        --name b2pool \
                        --resource-group mc-rg-Kangxh-AKS  \
                        --max-count 3 \
                        --min-count 1 \
                        --mode System 

    # scale to min size to save cost.
    az aks nodepool scale --cluster-name kangxhaksmc --resource-group mc-rg-Kangxh-AKS  --name b2pool --node-count 1

    # upgrade aks
    az aks get-upgrades --resource-group mc-rg-Kangxh-AKS  --name kangxhaksmc 
    az aks upgrade --resource-group mc-rg-Kangxh-AKS  --name kangxhaksmc --kubernetes-version 1.16.7

    # ensure the Mananged Identity has Contributor access to AKS and AKS Resources group.

## Internet access

    to reduce complexity, ingress controller is not used. 
    service exposed via public ip address.

## Deploy kangxh.com 

export SA_KEY=u8q18+A3xmibZ3LIP
export SA_NAME=kangxhsamc

kubectl create ns web

az acr login --name kangxhacrmc
az acr import --name kangxhacrmc --source docker.io/kangxh/kangxh.com:latest --image kangxh.com:latest

kubectl create secret generic kangxhsamc-secret --from-literal=azurestorageaccountname=$SA_NAME --from-literal=azurestorageaccountkey=$SA_KEY

kubectl apply -f kangxh.com.yaml