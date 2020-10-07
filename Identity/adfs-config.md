# Install ADFS

    1. install ADFS and config
        - farm: fs.kangxh.com
        - cert: *.kangxh.com
        - account: kangxh

    Message: 

    The SSL certificate subject alternative names do not support host name 'certauth.fs.kangxh.com'. Configuring certificate authentication binding on port '49443' and hostname 'fs.kangxh.com'

# Setup Relying Party Trust

   
# Customization
   
    1. Enable Sign In Page: Set-AdfsProperties -EnableIdPInitiatedSignonPage $true
    2. Change illustration: Set-AdfsWebTheme -TargetName default -Illustration @{path="c:\kangxh.com\illustration.jpg"}
    3. Sign In Description: Set-AdfsGlobalWebContent -SignInPageDescriptionText "<p>Only Domain User, UPN@kangxh.local is able to sign in. demo environment for ADFS</p>"

# Relying Party

    1. Add Relying Party Wizard with manual option: 
        - name: Kangxh.com Web
        - No Cert to encrypt claims
        - Enable WS-Fed Passive protocl: https://fs.kangxh.com/adfs/ls/
        - Enalbe SAML 2.0 WebSSO: https://www.kangxh.com/adfs/ls/
    
    2. Create Claim Issue
        - simple rule to return claim prerperties rule to retrun SPN and name. 

# Tools: 

    1. https://adfshelp.microsoft.com/ -> Claims X Ray

        $authzRules = "=>issue(Type = `"http://schemas.microsoft.com/authorization/claims/permit`", Value = `"true`"); "
        $issuanceRules = "@RuleName = `"Issue all claims`"`nx:[]=>issue(claim = x); "
        $redirectUrl = "https://adfshelp.microsoft.com/ClaimsXray/TokenResponse"
        $samlEndpoint = New-AdfsSamlEndpoint -Binding POST -Protocol SAMLAssertionConsumer -Uri $redirectUrl

        Add-ADFSRelyingPartyTrust -Name "ClaimsXray" -Identifier "urn:microsoft:adfs:claimsxray" -IssuanceAuthorizationRules $authzRules -IssuanceTransformRules $issuanceRules -WSFedEndpoint $redirectUrl -SamlEndpoint $samlEndpoint

        Add-AdfsClient -Name "ClaimsXrayClient" -ClientId "claimsxrayclient" -RedirectUri https://adfshelp.microsoft.com/ClaimsXray/TokenResponse

        if ([System.Environment]::OSVersion.Version.major -gt 6) { 
            Grant-AdfsApplicationPermission -ServerRoleIdentifier urn:microsoft:adfs:claimsxray -AllowAllRegisteredClients -ScopeNames "openid", "profile" 
        }

