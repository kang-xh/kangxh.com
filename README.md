# kangxh.com

## environment setup on azure, cross three tenants: 

    AIA-CSU-ALLENK
    admin: allenk@microsoft.com  
    usage: host most costing resource, AAD, storage, vm, app service, data solution, Management, Monitor

    MSDN-ALLENK
    admin: kang_xh@hotmail.com
    usage: host personal data, BCDR
    
    MC-CSU-ALLENK
    admin: allenk@ftachina.partner.onmschina.cn
    usage: necessary resource in China, mainly for local access accelerate. 

## naming convension

    PROJECT|Resource|Region|Usage[option]
    - kangxhnlbea-core
    - kangxhvm-dc

# Identity

    1. Domain registered via godaddy. 
    2. Onprem DC, kangxh.local, setup in China, 
    3. AAD Connect to sync to kangxh.com on MSDN. 
    4. ADFS enabled on China DC

# DevOps

    1. Use kangxhvmsea-dc to develop web site in WSL2
    2. Web site hosted on AKS container 
    3. Static content saved in Azure File 

# Architecture

![architecture](infra/kangxh.com-arch.png)