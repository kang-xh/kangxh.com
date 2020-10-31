# environment

    1. Use kangxhvmsea-dc as the main dev environment
    2. install WSL for web (flask) develop
    3. Jenkins on AKS cluster for CICD

# WSL

    Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
    $userenv = [System.Environment]::GetEnvironmentVariable("Path", "User")
    [System.Environment]::SetEnvironmentVariable("PATH", $userenv + ";C:\WSL\Ubuntu", "User")
