# environment

All the load running in the AKS cluster to save cost. 

    1. all the workload running on k8s pod to save cose.
    2. aks deployed in seperate vnet of dc and ds
    3. aks node is turn off on 10PM and boot at 8AM. 
    4. only one b2s node is booted if no specific request.    

## VM 

    1. kangxhvmsea-dc: onprem AD. connect to AAD
    2. kangxhvmsea-ds: data science vm.

## AKS

    1. kangxh.com
    2. ibean.org
    3. jenkins