import json
import re

from core.Authentication.Authentication import authWithProfile
from core.Other.PrintOutput.PrintOutput import printOutput

from core.Resources.Tags.ServiceFunctionsAndParameters import SERVICEFUNCTIONS



class BruteforceResources():
    def __init__(self, service, resourceARNsFile, profile):
        self.service = service
        self.profile = profile
        self.resourceARNsFile = resourceARNsFile
        self.resourceARNs = []
        self.SERVICEFUNCTIONS = {
    "acm-pca": {
        "list_tags": [
            "CertificateAuthorityArn"
        ]
    },
    "acm": {
        "list_tags_for_certificate": [
            "CertificateArn"
        ]
    },
    "apigateway": {
        "get_tags": [
            "resourceArn"
        ]
    },
    "apigatewayv2": {
        "get_tags": [
            "ResourceArn"
        ]
    },
    "backup": {
        "list_tags": [
            "ResourceArn"
        ]
    },
    "ce": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "cloudhsmv2": {
        "list_tags": [
            "ResourceId"
        ]
    },
    "cloudtrail": {
        "list_tags": [
            "ResourceIdList"
        ]
    },
    "connect": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "dax": {
        "list_tags": [
            "ResourceName"
        ]
    },
    "directconnect": {
        "describe_tags": [
            "resourceArns"
        ]
    },
    "dynamodb": {
        "list_tags_of_resource": [
            "ResourceArn"
        ]
    },
    "ecr-public": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "efs": {
        "list_tags_for_resource": [
            "ResourceId"
        ]
    },
    "elb": {
        "describe_tags": [
            "LoadBalancerNames"
        ]
    },
    "elbv2": {
        "describe_tags": [
            "ResourceArns"
        ]
    },
    "es": {
        "list_tags": [
            "ARN"
        ]
    },
    "firehose": {
        "list_tags_for_delivery_stream": [
            "DeliveryStreamName"
        ]
    },
    "glacier": {
        "list_tags_for_vault": [
            "vaultName"
        ]
    },
    "glue": {
        "get_tags": [
            "ResourceArn"
        ]
    },
    "kinesisvideo": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "kms": {
        "list_resource_tags": [
            "KeyId"
        ]
    },
    "lakeformation": {
        "get_resource_lf_tags": [
            "Resource"
        ]
    },
    "lambda": {
        "list_tags": [
            "Resource"
        ]
    },
    "logs": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "machinelearning": {
        "describe_tags": {
            "ResourceId": None,
            "ResourceType": [
                'BatchPrediction',
                'DataSource',
                'Evaluation',
                'MLModel'
            ]
        }
    },
    "memorydb": {
        "list_tags": [
            "ResourceArn"
        ]
    },
    "mq": {
        "list_tags": [
            "ResourceArn"
        ]
    },
    "opensearch": {
        "list_tags": [
            "ARN"
        ]
    },
    "opsworks": {
        "list_tags": [
            "ResourceArn"
        ]
    },
    "resource-groups": {
        "get_tags": [
            "Arn"
        ]
    },
    "route53": {
        "list_tags_for_resource": {
            "ResourceType": ['healthcheck', 'hostedzone'],
            "ResourceId": None
        }
    },
    "sagemaker": {
        "list_tags": [
            "ResourceArn"
        ]
    },
    "sqs": {
        "list_queue_tags": [
            "QueueUrl"
        ]
    },
    "workspaces": {
        "describe_tags": [
            "ResourceId"
        ]
    },
    "accessanalyzer": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "amp": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "amplify": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "appconfig": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "appfabric": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "appflow": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "appintegrations": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "application-autoscaling": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "application-insights": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "appmesh": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "apprunner": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "appstream": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "appsync": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "athena": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "auditmanager": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "b2bi": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "backup-gateway": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "batch": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "bcm-data-exports": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "bedrock-agent": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "bedrock": {
        "list_tags_for_resource": [
            "resourceARN"
        ]
    },
    "billingconductor": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "braket": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "chime-sdk-identity": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "chime-sdk-media-pipelines": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "chime-sdk-meetings": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "chime-sdk-messaging": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "chime-sdk-voice": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "cleanrooms": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "cleanroomsml": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "cloud9": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "clouddirectory": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "cloudfront": {
        "list_tags_for_resource": [
            "Resource"
        ]
    },
    "cloudhsm": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "cloudwatch": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "codeartifact": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "codecommit": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "codedeploy": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "codeguru-reviewer": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "codeguru-security": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "codeguruprofiler": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "codepipeline": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "codestar-connections": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "codestar-notifications": {
        "list_tags_for_resource": [
            "Arn"
        ]
    },
    "cognito-identity": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "cognito-idp": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "comprehend": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "config": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "connectcampaigns": {
        "list_tags_for_resource": [
            "arn"
        ]
    },
    "connectcases": {
        "list_tags_for_resource": [
            "arn"
        ]
    },
    "controltower": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "cur": {
        "list_tags_for_resource": [
            "ReportName"
        ]
    },
    "customer-profiles": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "databrew": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "dataexchange": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "datasync": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "datazone": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "detective": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "devicefarm": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "dlm": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "dms": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "docdb-elastic": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "docdb": {
        "list_tags_for_resource": [
            "ResourceName"
        ]
    },
    "drs": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "ds": {
        "list_tags_for_resource": [
            "ResourceId"
        ]
    },
    "ecr": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "ecs": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "eks": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "elasticache": {
        "list_tags_for_resource": [
            "ResourceName"
        ]
    },
    "elasticbeanstalk": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "emr-containers": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "emr-serverless": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "entityresolution": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "events": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "evidently": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "finspace": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "fis": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "fms": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "forecast": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "frauddetector": {
        "list_tags_for_resource": [
            "resourceARN"
        ]
    },
    "fsx": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "gamelift": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "globalaccelerator": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "grafana": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "greengrass": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "greengrassv2": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "groundstation": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "guardduty": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "healthlake": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "imagebuilder": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "inspector": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "inspector2": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "internetmonitor": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "iot": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "iotanalytics": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "iotdeviceadvisor": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "iotevents": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "iotfleethub": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "iotfleetwise": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "iotsecuretunneling": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "iotsitewise": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "iotthingsgraph": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "iottwinmaker": {
        "list_tags_for_resource": [
            "resourceARN"
        ]
    },
    "iotwireless": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "ivs-realtime": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "ivs": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "ivschat": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "kafka": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "kendra-ranking": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "kendra": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "keyspaces": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "kinesisanalytics": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "kinesisanalyticsv2": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "lex-models": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "lexv2-models": {
        "list_tags_for_resource": [
            "resourceARN"
        ]
    },
    "license-manager": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "location": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "lookoutequipment": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "lookoutmetrics": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "lookoutvision": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "m2": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "macie2": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "managedblockchain": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "marketplace-catalog": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "marketplace-deployment": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "mediaconnect": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "mediaconvert": {
        "list_tags_for_resource": [
            "Arn"
        ]
    },
    "medialive": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "mediapackage-vod": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "mediapackage": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "mediapackagev2": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "mediastore": {
        "list_tags_for_resource": [
            "Resource"
        ]
    },
    "mediatailor": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "medical-imaging": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "mgn": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "migration-hub-refactor-spaces": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "migrationhuborchestrator": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "mwaa": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "neptune-graph": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "neptune": {
        "list_tags_for_resource": [
            "ResourceName"
        ]
    },
    "network-firewall": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "networkmanager": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "networkmonitor": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "oam": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "omics": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "opensearchserverless": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "opsworkscm": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "organizations": {
        "list_tags_for_resource": [
            "ResourceId"
        ]
    },
    "osis": {
        "list_tags_for_resource": [
            "Arn"
        ]
    },
    "outposts": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "panorama": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "payment-cryptography": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "pca-connector-ad": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "personalize": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "pi": {
        "list_tags_for_resource": [
            "ServiceType",
            "ResourceARN"
        ]
    },
    "pinpoint-email": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "pinpoint-sms-voice-v2": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "pinpoint": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "pipes": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "proton": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "qbusiness": {
        "list_tags_for_resource": [
            "resourceARN"
        ]
    },
    "qconnect": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "qldb": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "quicksight": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "rbin": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "rds": {
        "list_tags_for_resource": [
            "ResourceName"
        ]
    },
    "redshift-serverless": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "rekognition": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "repostspace": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "resiliencehub": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "resource-explorer-2": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "robomaker": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "rolesanywhere": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "route53-recovery-control-config": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "route53-recovery-readiness": {
        "list_tags_for_resources": [
            "ResourceArn"
        ]
    },
    "route53resolver": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "rum": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "s3control": {
        "list_tags_for_resource": [
            "AccountId"
        ]
    },
    "sagemaker-geospatial": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "savingsplans": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "scheduler": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "schemas": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "securityhub": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "securitylake": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "service-quotas": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "servicecatalog-appregistry": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "servicediscovery": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "sesv2": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "shield": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "signer": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "simspaceweaver": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "snow-device-management": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "sns": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "ssm-contacts": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "ssm-incidents": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "ssm-sap": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "ssm": {
        "list_tags_for_resource": {
            "ResourceType": [
                'Document',
                'ManagedInstance',
                'MaintenanceWindow',
                'Parameter',
                'PatchBaseline',
                'OpsItem',
                'OpsMetadata',
                'Automation',
                'Association'
            ],
            "ResourceId": None
        }
    },
    "sso-admin": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "stepfunctions": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "storagegateway": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "swf": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "synthetics": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "textract": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "timestream-query": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "timestream-write": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "tnb": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "transcribe": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "transfer": {
        "list_tags_for_resource": [
            "Arn"
        ]
    },
    "translate": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "voice-id": {
        "list_tags_for_resource": [
            "ResourceArn"
        ]
    },
    "vpc-lattice": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "waf-regional": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "waf": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "wafv2": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "wellarchitected": {
        "list_tags_for_resource": [
            "WorkloadArn"
        ]
    },
    "wisdom": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "workmail": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    },
    "workspaces-thin-client": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "workspaces-web": {
        "list_tags_for_resource": [
            "resourceArn"
        ]
    },
    "xray": {
        "list_tags_for_resource": [
            "ResourceARN"
        ]
    }
}

    def bruteforceTask(self):
        self.readResourceARNFile()
        if self.service is not None:
            for resourceARN in self.resourceARNs:
                self.bruteforceService(
                    service=self.service,
                    resourceARN=resourceARN
                )

        else:
            for resourceARN in self.resourceARNs:
                service = self.getServiceFromArn(
                    resourceArn=resourceARN
                )
                if service is not None:
                    self.bruteforceService(
                        service=service,
                        resourceARN=resourceARN
                    )

    def readResourceARNFile(self):
        try:
            with open(self.resourceARNsFile) as resourceARNsFileObj:
                printOutput(False, f'Retrieving ARNs from file {self.resourceARNsFile}', 'success')
                self.resourceARNs = [i.replace("\n", '').strip() for i in resourceARNsFileObj.readlines()]
                printOutput(False, f'{len(self.resourceARNs)} ARNs retrieved from file {self.resourceARNsFile}', 'success')
                return True
        except Exception as e:
            printOutput(False, f"Error Reading ARNs from Resource File: {str(e)}", "failure")
            return False

    def getServiceFromArn(self, resourceArn):
        if not re.match(resourceArn, 'arn:aws[a-zA-Z-]*:[a-z0-9-]*:[a-z0-9-]*:[0-9]{12}:[^ \n]+'):
            printOutput(False, f"Resource {resourceArn} is not an ARN", "failure")
            return None

        try:
            return resourceArn.split(":")[2].split("/")[0]
        except Exception as e:
            printOutput(False, f"Error Getting Service Type from ARN: {str(e)}", "failure")
            return None

    def getResourceTypeFromArn(self, resourceArn):
        if not re.match(resourceArn, 'arn:aws[a-zA-Z-]*:[a-z0-9-]*:[a-z0-9-]*:[0-9]{12}:[^ \n]+'):
            printOutput(False, f"Resource {resourceArn} is not an ARN", "failure")
            return None

        try:
            return resourceArn.split(":")[5].split("/")[0]
        except Exception as e:
            printOutput(False, f"Error Getting Resource Type from ARN: {str(e)}", "failure")
            return None

    def bruteforceSingleResource(self, resourceARN, functionName, args, service):
        client = authWithProfile(
            Profile=self.profile,
            Service=service
        )
        if client is not None:
            try:
                tags = getattr(client, functionName)(**args)
                if 'ResponseMetadata' in tags:
                    del(tags['ResponseMetadata'])
                printOutput(False, f"Resource {resourceARN} exists", 'success')
                print(
                    json.dumps(
                        tags, indent=4, default=str
                    )
                )
                return True

                """
                except client.exceptions.ResourceNotFoundFault:
                return False"""

            except Exception as e:
                if "InvalidInput" in str(e) or \
                        "ValidationException" in str(e) or \
                        "NoSuchHealthCheck" in str(e) or \
                    "InvalidResourceId" in str(e):
                    printOutput(
                        False, f"Resource {resourceARN} does not exist: {str(e)}", "failure"
                    )
                    return False
                else:
                    printOutput(False, f"Error Bruteforcing resource {resourceARN} in service {service} " + str(e).replace("\n", ''), 'failure')
                return False

    def getNamefromARN(self, resourceArn):
        try:
            return resourceArn.split("/")[1]
        except Exception as e:
            printOutput(False, f"Error Getting Name from ARN: {str(e)}", "failure")
            return None

    def bruteforceService(self, service, resourceARN):
        if len(self.resourceARNs) == 0:
            printOutput(
                False, f"No ARN Retrieved from file {self.resourceARNsFile}", 'failure'
            )

        if service not in self.SERVICEFUNCTIONS:
            printOutput(
                False, f"Cannot look at {resourceARN} as the service {service} does not allow for tag based enumeration",
                'failure')
            return

        serviceDefinitions = self.SERVICEFUNCTIONS[service]

        for functionName, parameters in serviceDefinitions.items():
            try:
                args = {}
                resourceTypeParameter = None
                resourceType = None
                if type(parameters) == list:
                    if len(parameters) > 0:
                        if 'name' in parameters[0]:
                            resourceName = self.getNamefromARN(resourceARN)
                            args[parameters[0]] = resourceName

                        elif parameters[0] == "ResourceIdList":
                            args[parameters[0]] = [resourceARN]

                        else:
                            args[parameters[0]] = resourceARN

                    self.bruteforceSingleResource(
                        resourceARN=resourceARN,
                        args=args,
                        functionName=functionName,
                        service=service
                    )

                elif type(parameters) == dict:
                    for parameter, value in parameters.items():
                        if parameter.lower() == 'resourcetype':
                            resourceTypeParameter = parameter
                            resourceType = self.getResourceTypeFromArn(resourceARN)
                            if resourceType is None or resourceType not in parameters[parameter]:
                                resourceType = None
                                continue
                            else:
                                args[parameter] = resourceType
                        else:
                            if 'name' in parameter:
                                resourceName = self.getNamefromARN(resourceARN)
                                args[parameter] = resourceName
                            else:
                                args[parameter] = resourceARN

                    if resourceType is not None:
                        for predefinedResourceType in parameters[resourceTypeParameter]:
                            args[resourceTypeParameter] = predefinedResourceType
                            self.bruteforceSingleResource(
                                resourceARN=resourceARN,
                                args=args,
                                functionName=functionName,
                                service=service
                            )

                    else:
                        self.bruteforceSingleResource(
                            resourceARN=resourceARN,
                            args=args,
                            functionName=functionName,
                            service=service
                        )

            except Exception as e:
                printOutput(False, f"Error Bruteforcing Resource {resourceARN}: {str(e)}", "failure")

