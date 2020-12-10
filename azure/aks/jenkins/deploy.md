 # jenkins storage  

    use file share as jenkins storage. as the default access level is 0755, create PV to change it to 0777  

    kubectl apply -f jenkins.yaml  

# Jenkins Admin  

    kubectl exec jenkins-5787bd657f-8hrr9 -- cat /var/jenkins_home/secrets/initialAdminPassword
