# Infrastructure

    MSDN subscription is mainly used for BCDR. Thus, limit resource usage in this subscription.

## AKS

    az extension add --name aks-preview

    # get dependent resource ID
    SUBNET=$(az network vnet subnet show --resource-group MSDN-RG-Kangxh-Core --vnet-name kangxhvnetsea --name aks --query id -o tsv)
    PIP=$(az network public-ip show --resource-group  MSDN-RG-Kangxh-AKS --name kangxhpipsea-aks --query id -o tsv)

    # Create AKS, --node-resource-group is not supported in China yet.
    
    az aks create --resource-group MSDN-RG-Kangxh-AKS \
        --name kangxhakssea \
        --ssh-key-value  /mnt/c/kangxh/AzureLabs/SSHKey/common/id_rsa.pub \
        --admin-username kangxh \
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

    # donwload kubectl credential
    az aks get-credentials --resource-group MSDN-RG-Kangxh-AKS  --name kangxhakssea

## Deploy workload

    export SA_KEY=ABCDABCDABCDABCDABCDABCD
    export SA_NAME=kangxhsasea

    kubectl create secret generic kangxhsasea-secret --from-literal=azurestorageaccountname=$SA_NAME --from-literal=azurestorageaccountkey=$SA_KEY

    # transfer docker image from docker.io/kangxh to kangxhacrsea
    az acr login --name kangxhacrsea
    az acr import --name kangxhacrsea --source docker.io/kangxh/kangxh.com:latest --image kangxh.com:latest
    az acr import --name kangxhacrsea --source docker.io/kangxh/ibean.org:latest --image ibean.org:latest

    kubectl apply -f kangxh.com.yaml
    kubectl apply -f ibean.org.yaml

