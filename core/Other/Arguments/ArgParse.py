import argparse

from core.Other.Arguments.Banner import printBanner


def parseArgs():
    printBanner()
    parser = argparse.ArgumentParser(
        prog='TagNabIt',
        description='TagNabIt is a tool designed to find which identities can enumerate and Bruteforce Cloud Resources using AWS Tags.',
    )

    subparsers = parser.add_subparsers(dest='command',
                                       help="Select command to work with.",
                                       # choices=['ENUMERATE', 'FINDPOLICIES', 'FINDUSERS']
                                       )

    # -----------------------------------------------------------
    # BRUTEFORCEIAM
    # -----------------------------------------------------------
    bruteforceiamparser = subparsers.add_parser('BRUTEFORCEIAM',
                                             help='Bruteforce account IAM Resources using tags')
    bruteforceiamparser.add_argument('-p', '--profile', required=True, default="default")
    bruteforceiamparser.add_argument('-r', '--region', required=True)
    bruteforceiamparser.add_argument('-rf', '--resource-file', required=True)
    bruteforceiamparser.add_argument('-rt', '--resource-type', required=True, choices=[
        "user",
        "serial-number",
        "openid-provider",
        "policy",
        "role",
        "saml-provider",
        "server-certificate"
    ])
    bruteforceiamparser.add_argument('-v', '--verbose', help="Get extra output of the tool", action="store_true")

    # -----------------------------------------------------------
    # BRUTEFORCERESOURCES
    # -----------------------------------------------------------
    bruteforceparser = subparsers.add_parser('BRUTEFORCERESOURCES',
                                            help='Bruteforce account Resources using service specific tag API calls'
                                                 '')
    bruteforceparser.add_argument('-p', '--profile', required=True, default="default")
    bruteforceparser.add_argument('-r', '--region', required=True)
    bruteforceparser.add_argument('-s', '--service', choices=[
        'acm-pca', 'acm', 'apigateway', 'apigatewayv2', 'autoscaling', 'backup', 'ce', 'cloudhsmv2', 'cloudtrail', 'connect', 'dax', 'directconnect', 'discovery', 'dynamodb',
        'ec2', 'ecr-public', 'efs', 'elb', 'elbv2', 'es', 'firehose', 'glacier', 'glue', 'kinesisvideo', 'kms', 'lakeformation', 'lambda', 'logs', 'machinelearning', 'memorydb',
        'mq', 'opensearch', 'opsworks', 'redshift', 'resource-groups', 'route53', 'route53domains', 'sagemaker', 'sqs', 'workspaces', 'accessanalyzer', 'amp', 'amplify', 'appconfig',
        'appfabric', 'appflow', 'appintegrations', 'application-autoscaling', 'application-insights', 'appmesh', 'apprunner', 'appstream', 'appsync', 'athena', 'auditmanager', 'b2bi',
        'backup-gateway', 'batch', 'bcm-data-exports', 'bedrock-agent', 'bedrock', 'billingconductor', 'braket', 'chime-sdk-identity', 'chime-sdk-media-pipelines', 'chime-sdk-meetings',
        'chime-sdk-messaging', 'chime-sdk-voice', 'cleanrooms', 'cleanroomsml', 'cloud9', 'clouddirectory', 'cloudfront', 'cloudhsm', 'cloudwatch', 'codeartifact', 'codecommit', 'codedeploy',
        'codeguru-reviewer', 'codeguru-security', 'codeguruprofiler', 'codepipeline', 'codestar-connections', 'codestar-notifications', 'cognito-identity', 'cognito-idp', 'comprehend', 'config',
        'connectcampaigns', 'connectcases', 'controltower', 'cur', 'customer-profiles', 'databrew', 'dataexchange', 'datasync', 'datazone', 'detective', 'devicefarm', 'dlm', 'dms', 'docdb-elastic',
        'docdb', 'drs', 'ds', 'ecr', 'ecs', 'eks', 'elasticache', 'elasticbeanstalk', 'emr-containers', 'emr-serverless', 'entityresolution', 'events', 'evidently', 'finspace', 'fis', 'fms', 'forecast',
        'frauddetector', 'fsx', 'gamelift', 'globalaccelerator', 'grafana', 'greengrass', 'greengrassv2', 'groundstation', 'guardduty', 'healthlake', 'imagebuilder', 'inspector', 'inspector2', 'internetmonitor',
        'iot', 'iotanalytics', 'iotdeviceadvisor', 'iotevents', 'iotfleethub', 'iotfleetwise', 'iotsecuretunneling', 'iotsitewise', 'iotthingsgraph', 'iottwinmaker', 'iotwireless', 'ivs-realtime', 'ivs', 'ivschat',
        'kafka', 'kendra-ranking', 'kendra', 'keyspaces', 'kinesisanalytics', 'kinesisanalyticsv2', 'lex-models', 'lexv2-models', 'license-manager', 'location', 'lookoutequipment', 'lookoutmetrics', 'lookoutvision',
        'm2', 'macie2', 'managedblockchain', 'marketplace-catalog', 'marketplace-deployment', 'mediaconnect', 'mediaconvert', 'medialive', 'mediapackage-vod', 'mediapackage', 'mediapackagev2', 'mediastore', 'mediatailor',
        'medical-imaging', 'mgn', 'migration-hub-refactor-spaces', 'migrationhuborchestrator', 'mwaa', 'neptune-graph', 'neptune', 'network-firewall', 'networkmanager', 'networkmonitor', 'oam', 'omics',
        'opensearchserverless', 'opsworkscm', 'organizations', 'osis', 'outposts', 'panorama', 'payment-cryptography', 'pca-connector-ad', 'personalize', 'pi', 'pinpoint-email', 'pinpoint-sms-voice-v2',
        'pinpoint', 'pipes', 'proton', 'qbusiness', 'qconnect', 'qldb', 'quicksight', 'rbin', 'rds', 'redshift-serverless', 'rekognition', 'repostspace', 'resiliencehub', 'resource-explorer-2', 'robomaker',
        'rolesanywhere', 'route53-recovery-control-config', 'route53-recovery-readiness', 'route53resolver', 'rum', 's3control', 'sagemaker-geospatial', 'savingsplans', 'scheduler', 'schemas', 'securityhub',
        'securitylake', 'service-quotas', 'servicecatalog-appregistry', 'servicediscovery', 'sesv2', 'shield', 'signer', 'simspaceweaver', 'snow-device-management', 'sns', 'ssm-contacts', 'ssm-incidents',
        'ssm-sap', 'ssm', 'sso-admin', 'stepfunctions', 'storagegateway', 'swf', 'synthetics', 'textract', 'timestream-query', 'timestream-write', 'tnb', 'transcribe', 'transfer', 'translate', 'voice-id',
        'vpc-lattice', 'waf-regional', 'waf', 'wafv2', 'wellarchitected', 'wisdom', 'workmail', 'workspaces-thin-client', 'workspaces-web', 'xray'
    ])
    bruteforceparser.add_argument('-rf', '--resource-arn-file', required=True)
    bruteforceparser.add_argument('-v', '--verbose', help="Get extra output of the tool", action="store_true")

    # -----------------------------------------------------------
    # CHECKUSAGE
    # -----------------------------------------------------------
    checkusageparser = subparsers.add_parser('CHECKUSAGE',
                                             help='Check if any identity has executed tag enumerate/bruteforce on the Account and dump it.')
    checkusageparser.add_argument('-p', '--profile',
                                  default="default")
    checkusageparser.add_argument('-v', '--verbose', help="Get extra output of the tool", action="store_true")

    # -----------------------------------------------------------
    # ENUMERATE
    # -----------------------------------------------------------
    enumerateparser = subparsers.add_parser('ENUMERATERESOURCES',
                                             help='Enumerate account using API request that do not require input')
    enumerateparser.add_argument('-p', '--profile',
                                  default="default")
    enumerateparser.add_argument('-v', '--verbose', help="Get extra output of the tool", action="store_true")

    return parser.parse_args()

