# create newest build
docker image build -t kangxh.com:test -f ~/github/py-kangxh.com/docker/Dockerfile ~/github/py-kangxh.com/

# start the web site in WSL2 docker
docker run -d --rm -p 2000:80  kangxh.com:test 

docker run -it --rm -p 2000:80  kangxh.com:test bash

# access from WSL2 Host server to test the web site. http://localhost:2000

# push the tested version to ACR 
az acr login --name kangxhacrsea
docker tag kangxh.com:test kangxhacrsea.azurecr.io/kangxh.com:latest && docker push kangxhacrsea.azurecr.io/kangxh.com:latest
