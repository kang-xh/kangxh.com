# create newest build
docker image build -t kangxh.com:latest -f /mnt/c/Users/allenk/repos/kangxh.com/web/docker/Dockerfile /mnt/c/Users/allenk/repos/kangxh.com/web

az acr login --name kangxhacrsea

docker push kangxh/kangxh.com:latest 
docker tag kangxh/kangxh.com:latest kangxhacrsea.azurecr.io/kangxh.com:latest 
docker push kangxhacrsea.azurecr.io/kangxh.com:latest
