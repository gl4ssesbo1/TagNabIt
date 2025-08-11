import json
import re
import boto3, botocore

from core.Authentication.Authentication import authWithProfile
from core.Other.PrintOutput.PrintOutput import printOutput

class BruteforceIAM():
    def __init__(self, profile, resourceARNsFile, resourceType, accountID, region):
        self.profile = profile
        self.resourceARNsFile = resourceARNsFile
        self.resourceARNs = []
        self.resourceType = resourceType
        self.accountID = accountID
        self.region = region

        self.iamClient = authWithProfile(Profile=self.profile, Service='iam')

        self.IAMFUNCTIONS = {
            "list_instance_profile_tags": [
                "InstanceProfileName"
            ],
            "list_mfa_device_tags": [
                "SerialNumber"
            ],
            "list_open_id_connect_provider_tags": [
                "OpenIDConnectProviderArn"
            ],
            "list_policy_tags": [
                "PolicyArn"
            ],
            "list_role_tags": [
                "RoleName"
            ],
            "list_saml_provider_tags": [
                "SAMLProviderArn"
            ],
            "list_server_certificate_tags": [
                "ServerCertificateName"
            ],
            "list_user_tags": [
                "UserName"
            ]
        }

    def generatePolicyARN(self, policyName, accountID):
        if re.search('^arn:aws:iam::[0-9]{12}:policy/[a-zA-Z_+=,.@-/]{1,}', policyName):
            return policyName
        else:
            return f'arn:aws:iam::{accountID}:policy/{policyName}'

    def generateSAMLProviderArn(self, samlProviderName, accountID):
        if re.search('^arn:aws:iam::[0-9]{12}:saml-provider/[a-zA-Z_+=,.@-/]{1,}'):
            return samlProviderName
        else:
            return f'arn:aws:iam::{accountID}:saml-provider/{samlProviderName}'

    def bruteforceIAM(self, profile, functionName, arguments, resourceArn):
        #client = None
        #session = boto3.Session(profile_name=profile)
        #try:
        #    client = session.client("iam", region_name=self.region)
        #except Exception as e:
        #    printOutput(True, f"Error Creating a boto client: {str(e)}", 'failure')

        try:
            # print(client.list_tags_for_resource(ResourceARN=resourceArn))
            response = getattr(self.iamClient, functionName)(**arguments)
            if 'ResponseMetadata' in response:
                del (response['ResponseMetadata'])
            printOutput(True, f"Resource Found: '{resourceArn}'", 'success')
            print(json.dumps(response, indent=4, default=str))
            return True

        except self.iamClient.exceptions.InvalidInputException as e:
            exceptionstring = str(e).replace('\n', ' ')
            printOutput(True, f"Error for {resourceArn}: {exceptionstring}", 'failure')
            return False

        except botocore.exceptions.ParamValidationError as e:
            exceptionstring = str(e).replace('\n', ' ')
            printOutput(True, f"Error for {resourceArn}: {exceptionstring}", 'failure')
            return False
        # except botocore.errorfactory.NoSuchEntityException:
        #    return False

        except self.iamClient.exceptions.NoSuchEntityException:
            return False

        except self.iamClient.exceptions.ResourceNotFoundFault:
            return False

        except Exception as e:
            printOutput(True, str(e), 'failure')

    def generateFunctionArgs(self, resourceArn, resourceType, accountID):
        if resourceType == "user":
            return {
                "UserName": resourceArn
            }, "list_user_tags"

        elif resourceType == "serial-number":
            return {
                "SerialNumber": resourceArn
            }, "list_mfa_device_tags"

        elif resourceType == "openid-provider":
            return {
                "OpenIDConnectProviderArn": resourceArn
            }, "list_open_id_connect_provider_tags"

        elif resourceType == "policy":
            resourceArn = self.generatePolicyARN(policyName=resourceArn, accountID=accountID)
            return {
                "PolicyArn": resourceArn
            }, "list_policy_tags"

        elif resourceType == "role":
            return {
                "RoleName": resourceArn
            }, "list_role_tags"

        elif resourceType == "saml-provider":
            resourceArn = self.generateSAMLProviderArn(samlProviderName=resourceArn, accountID=accountID)
            return {
                "SAMLProviderArn": resourceArn
            }, "list_saml_provider_tags"

        elif resourceType == "server-certificate":
            return {
                "ServerCertificateName": resourceArn
            }, "list_server_certificate_tags"

        else:
            return None, None

    def bruteforceIAMMain(self):
        try:
            with open(self.resourceARNsFile) as resource_arn_fileobj:
                resourcearnslines = resource_arn_fileobj.readlines()
                resourcearns = [i.replace("\n", '').strip() for i in resourcearnslines]



            for resourcearn in resourcearns:
                arguments, functionName = self.generateFunctionArgs(
                    resourceArn=resourcearn, resourceType=self.resourceType, accountID=self.accountID
                )
                self.bruteforceIAM(self.profile, functionName, arguments, resourcearn)

            return True

        except Exception as e:
            printOutput(True, f"Error: {str(e)}", 'failure')
            return False

