# Resource Deployment

## management spn: 

    $azRoot = Get-ChildItem -Path Cert:\LocalMachine\my\7D9DF109D674DB73D72032D8EA6D1C4AD0A39C6C
    New-SelfSignedCertificate -certstorelocation cert:\localmachine\my -dnsname "az-cli-spn-allenk-2037" -Signer $azRoot

az cloud set --name AzureCloud

az login

72f988bf-86f1-41af-91ab-2d7cd011db47

az ad sp create-for-rbac --name az-cli-spn-global-allenk-2037 --cert @C:\kangxh\AzureLabs\Certs\az-cli-spn-global-allenk-2037.pem

# setup environment

54b20299-30ca-44c8-b4c6-96f8d11f16d1

    az cloud set AzureCloud
    az login --service-principal --username APP_ID --tenant TENANT_ID --password /path/to/cert
    az connect 
    as configure location=eastasia
    az config default location

# create resource group


# 