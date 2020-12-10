# create newest build
docker image build -t kangxh/kangxh.com:latest -f /mnt/c/Users/allenk/repos/wsl/kangxh.com/web/docker/Dockerfile /mnt/c/Users/allenk/repos/wsl/kangxh.com/web

docker push kangxh/kangxh.com:latest 

az acr login --name kangxhacrsea
docker tag kangxh/kangxh.com:latest kangxhacrsea.azurecr.io/kangxh.com:latest 
docker push kangxhacrsea.azurecr.io/kangxh.com:latest

az acr login --name kangxhacrmc
docker tag kangxh/kangxh.com:latest kangxhacrmc.azurecr.cn/kangxh.com:latest 
docker push kangxhacrmc.azurecr.cn/kangxh.com:latest


