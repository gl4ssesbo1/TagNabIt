import json, os
import datetime

import boto3

from core.Authentication.Authentication import authWithProfile
from core.Other.PrintOutput.PrintOutput import printOutput
from core.Resources.OutputDump.OutputDump import dumpCSV


class CheckUsage:
    def __init__(self, profile, verbose, accountID):
        self.verbose = verbose
        self.profile = profile
        self.accountID = accountID
        self.client = authWithProfile(
            Profile=self.profile,
            Service="cloudtrail"
        )

        self.eventsToDetect = [
            'resourcegroupstaggingapi:GetResources','acm-pca:ListTags', 'acm:ListTagsForCertificate', 'apigateway:GetTags', 'apigatewayv2:GetTags', 'autoscaling:DescribeTags', 'backup:ListTags', 'ce:ListTagsForResource',
            'cloudhsmv2:ListTags', 'cloudtrail:ListTags', 'connect:ListTagsForResource', 'dax:ListTags', 'directconnect:DescribeTags', 'discovery:DescribeTags', 'dynamodb:ListTagsOfResource',
            'ec2:DescribeTags', 'ecr-public:ListTagsForResource', 'efs:DescribeTags', 'efs:ListTagsForResource', 'elb:DescribeTags', 'elbv2:DescribeTags', 'es:ListTags',
            'firehose:ListTagsForDeliveryStream', 'glacier:ListTagsForVault', 'glue:GetTags', 'kinesisvideo:ListTagsForResource', 'kms:ListResourceTags', 'lakeformation:GetResourceLfTags',
            'lambda:ListTags', 'logs:ListTagsLogGroup', 'logs:ListTagsForResource', 'machinelearning:DescribeTags', 'memorydb:ListTags', 'mq:ListTags', 'opensearch:ListTags', 'opsworks:ListTags',
            'redshift:DescribeTags', 'resource-groups:GetTags', 'route53:ListTagsForResource', 'route53domains:ListTagsForDomain', 'sagemaker:ListTags', 'sqs:ListQueueTags', 'workspaces:DescribeTags',
            'accessanalyzer:ListTagsForResource', 'amp:ListTagsForResource', 'amplify:ListTagsForResource', 'appconfig:ListTagsForResource', 'appfabric:ListTagsForResource', 'appflow:ListTagsForResource',
            'appintegrations:ListTagsForResource', 'application-autoscaling:ListTagsForResource', 'application-insights:ListTagsForResource', 'appmesh:ListTagsForResource', 'apprunner:ListTagsForResource',
            'appstream:ListTagsForResource', 'appsync:ListTagsForResource', 'athena:ListTagsForResource', 'auditmanager:ListTagsForResource', 'b2bi:ListTagsForResource', 'backup-gateway:ListTagsForResource',
            'batch:ListTagsForResource', 'bcm-data-exports:ListTagsForResource', 'bedrock-agent:ListTagsForResource', 'bedrock:ListTagsForResource', 'billingconductor:ListTagsForResource',
            'braket:ListTagsForResource', 'chime-sdk-identity:ListTagsForResource', 'chime-sdk-media-pipelines:ListTagsForResource', 'chime-sdk-meetings:ListTagsForResource', 'chime-sdk-messaging:ListTagsForResource',
            'chime-sdk-voice:ListTagsForResource', 'cleanrooms:ListTagsForResource', 'cleanroomsml:ListTagsForResource', 'cloud9:ListTagsForResource', 'clouddirectory:ListTagsForResource',
            'cloudfront:ListTagsForResource', 'cloudhsm:ListTagsForResource', 'cloudwatch:ListTagsForResource', 'codeartifact:ListTagsForResource', 'codecommit:ListTagsForResource',
            'codedeploy:ListTagsForResource', 'codeguru-reviewer:ListTagsForResource', 'codeguru-security:ListTagsForResource', 'codeguruprofiler:ListTagsForResource', 'codepipeline:ListTagsForResource',
            'codestar-connections:ListTagsForResource', 'codestar-notifications:ListTagsForResource', 'cognito-identity:ListTagsForResource', 'cognito-idp:ListTagsForResource', 'comprehend:ListTagsForResource',
            'config:ListTagsForResource', 'connectcampaigns:ListTagsForResource', 'connectcases:ListTagsForResource', 'controltower:ListTagsForResource', 'cur:ListTagsForResource', 'customer-profiles:ListTagsForResource',
            'databrew:ListTagsForResource', 'dataexchange:ListTagsForResource', 'datasync:ListTagsForResource', 'datazone:ListTagsForResource', 'detective:ListTagsForResource', 'devicefarm:ListTagsForResource',
            'dlm:ListTagsForResource', 'dms:ListTagsForResource', 'docdb-elastic:ListTagsForResource', 'docdb:ListTagsForResource', 'drs:ListTagsForResource', 'ds:ListTagsForResource', 'ecr:ListTagsForResource',
            'ecs:ListTagsForResource', 'eks:ListTagsForResource', 'elasticache:ListTagsForResource', 'elasticbeanstalk:ListTagsForResource', 'emr-containers:ListTagsForResource', 'emr-serverless:ListTagsForResource',
            'entityresolution:ListTagsForResource', 'events:ListTagsForResource', 'evidently:ListTagsForResource', 'finspace:ListTagsForResource', 'fis:ListTagsForResource', 'fms:ListTagsForResource',
            'forecast:ListTagsForResource', 'frauddetector:ListTagsForResource', 'fsx:ListTagsForResource', 'gamelift:ListTagsForResource', 'globalaccelerator:ListTagsForResource',
            'grafana:ListTagsForResource', 'greengrass:ListTagsForResource', 'greengrassv2:ListTagsForResource', 'groundstation:ListTagsForResource', 'guardduty:ListTagsForResource',
            'healthlake:ListTagsForResource', 'imagebuilder:ListTagsForResource', 'inspector:ListTagsForResource', 'inspector2:ListTagsForResource', 'internetmonitor:ListTagsForResource', 'iot:ListTagsForResource',
            'iotanalytics:ListTagsForResource', 'iotdeviceadvisor:ListTagsForResource', 'iotevents:ListTagsForResource', 'iotfleethub:ListTagsForResource', 'iotfleetwise:ListTagsForResource',
            'iotsecuretunneling:ListTagsForResource', 'iotsitewise:ListTagsForResource', 'iotthingsgraph:ListTagsForResource', 'iottwinmaker:ListTagsForResource', 'iotwireless:ListTagsForResource',
            'ivs-realtime:ListTagsForResource', 'ivs:ListTagsForResource', 'ivschat:ListTagsForResource', 'kafka:ListTagsForResource', 'kendra-ranking:ListTagsForResource', 'kendra:ListTagsForResource',
            'keyspaces:ListTagsForResource', 'kinesisanalytics:ListTagsForResource', 'kinesisanalyticsv2:ListTagsForResource', 'lex-models:ListTagsForResource', 'lexv2-models:ListTagsForResource',
            'license-manager:ListTagsForResource', 'location:ListTagsForResource', 'lookoutequipment:ListTagsForResource', 'lookoutmetrics:ListTagsForResource', 'lookoutvision:ListTagsForResource',
            'm2:ListTagsForResource', 'macie2:ListTagsForResource', 'managedblockchain:ListTagsForResource', 'marketplace-catalog:ListTagsForResource', 'marketplace-deployment:ListTagsForResource',
            'mediaconnect:ListTagsForResource', 'mediaconvert:ListTagsForResource', 'medialive:ListTagsForResource', 'mediapackage-vod:ListTagsForResource', 'mediapackage:ListTagsForResource',
            'mediapackagev2:ListTagsForResource', 'mediastore:ListTagsForResource', 'mediatailor:ListTagsForResource', 'medical-imaging:ListTagsForResource', 'mgn:ListTagsForResource',
            'migration-hub-refactor-spaces:ListTagsForResource', 'migrationhuborchestrator:ListTagsForResource', 'mwaa:ListTagsForResource', 'neptune-graph:ListTagsForResource', 'neptune:ListTagsForResource',
            'network-firewall:ListTagsForResource', 'networkmanager:ListTagsForResource', 'networkmonitor:ListTagsForResource', 'oam:ListTagsForResource', 'omics:ListTagsForResource', 'opensearchserverless:ListTagsForResource',
            'opsworkscm:ListTagsForResource', 'organizations:ListTagsForResource', 'osis:ListTagsForResource', 'outposts:ListTagsForResource', 'panorama:ListTagsForResource', 'payment-cryptography:ListTagsForResource',
            'pca-connector-ad:ListTagsForResource', 'personalize:ListTagsForResource', 'pi:ListTagsForResource', 'pinpoint-email:ListTagsForResource', 'pinpoint-sms-voice-v2:ListTagsForResource', 'pinpoint:ListTagsForResource',
            'pipes:ListTagsForResource', 'proton:ListTagsForResource', 'qbusiness:ListTagsForResource', 'qconnect:ListTagsForResource', 'qldb:ListTagsForResource', 'quicksight:ListTagsForResource', 'rbin:ListTagsForResource',
            'rds:ListTagsForResource', 'redshift-serverless:ListTagsForResource', 'rekognition:ListTagsForResource', 'repostspace:ListTagsForResource', 'resiliencehub:ListTagsForResource', 'resource-explorer-2:ListTagsForResource',
            'robomaker:ListTagsForResource', 'rolesanywhere:ListTagsForResource', 'route53-recovery-control-config:ListTagsForResource', 'route53-recovery-readiness:ListTagsForResources', 'route53resolver:ListTagsForResource',
            'rum:ListTagsForResource', 's3control:ListTagsForResource', 'sagemaker-geospatial:ListTagsForResource', 'savingsplans:ListTagsForResource', 'scheduler:ListTagsForResource', 'schemas:ListTagsForResource',
            'securityhub:ListTagsForResource', 'securitylake:ListTagsForResource', 'service-quotas:ListTagsForResource', 'servicecatalog-appregistry:ListTagsForResource', 'servicediscovery:ListTagsForResource',
            'sesv2:ListTagsForResource', 'shield:ListTagsForResource', 'signer:ListTagsForResource', 'simspaceweaver:ListTagsForResource', 'snow-device-management:ListTagsForResource', 'sns:ListTagsForResource',
            'ssm-contacts:ListTagsForResource', 'ssm-incidents:ListTagsForResource', 'ssm-sap:ListTagsForResource', 'ssm:ListTagsForResource', 'sso-admin:ListTagsForResource', 'stepfunctions:ListTagsForResource',
            'storagegateway:ListTagsForResource', 'swf:ListTagsForResource', 'synthetics:ListTagsForResource', 'textract:ListTagsForResource', 'timestream-query:ListTagsForResource', 'timestream-write:ListTagsForResource',
            'tnb:ListTagsForResource', 'transcribe:ListTagsForResource', 'transfer:ListTagsForResource', 'translate:ListTagsForResource', 'voice-id:ListTagsForResource', 'vpc-lattice:ListTagsForResource',
            'waf-regional:ListTagsForResource', 'waf:ListTagsForResource', 'wafv2:ListTagsForResource', 'wellarchitected:ListTagsForResource', 'wisdom:ListTagsForResource', 'workmail:ListTagsForResource',
            'workspaces-thin-client:ListTagsForResource', 'workspaces-web:ListTagsForResource', 'xray:ListTagsForResource'
        ]


    def check_usage(self):
        logs = []
        printOutput(
            True,
            "Finding usage of tag bruteforce on logs",
            "loading"
        )
        for eventCombo in self.eventsToDetect:

            logs.extend(
                self.list_log_event(eventCombo)
            )

        if logs is not None:
            #tablePrintObj.logsTablePrint(logs, self.args.verbose)
            if dumpCSV(logs, self.accountID, "cloudtraillogs", [
                'EventTime',
                'EventName',
                'Username',
                'AccessKeyId',
                'AccountID',
                'SourceIP',
                'UserAgent',
                'ErrorCode',
                'ErrorMessage'
            ]):
                printOutput(True, f"Logs saved to ./output/{self.accountID}/cloudtraillogs.csv","success")

    def list_log_event(self, eventCombo):
        printOutput(
            True,
            f"Finding usage of {eventCombo} in logs",
            "loading"
        )
        loglist = []

        eventName = eventCombo.split(":")[1].replace('\n', '').strip()
        service = eventCombo.split(":")[0].replace('\n', '').strip()

        eventService = boto3.Session(profile_name=self.profile).client(service).meta.endpoint_url.split('/')[2].split(".")[0].replace('\n', '').strip()
        eventSource = f"{eventService}.amazonaws.com"

        try:
            startTime = datetime.datetime.now() - datetime.timedelta(days=90)
            response = self.client.lookup_events(
                LookupAttributes=[
                    {
                        'AttributeKey': 'EventName',
                        'AttributeValue': eventName
                    }
                ],
                StartTime=startTime
            )
            logs = response['Events']
            while "NextToken" in response:
                response = self.client.lookup_events(
                    LookupAttributes=[
                        {
                            'AttributeKey': 'EventName',
                            'AttributeValue': eventName
                        }
                    ],
                    StartTime=startTime,
                    NextToken=response["NextToken"]
                )
                logs.extend(response['Events'])


            for event in logs:
                if event['EventSource'] == eventSource:
                    logdata = {
                        'EventTime': event['EventTime'],
                        'EventSource': event['EventSource'],
                        'EventName': event['EventName'],
                        'Arn': json.loads(event['CloudTrailEvent'])['userIdentity']['arn'],
                        'AccessKeyId': event['AccessKeyId'],
                        'AccountID': json.loads(event['CloudTrailEvent'])['userIdentity']['accountId'],
                        'SourceIP': json.loads(event['CloudTrailEvent'])['sourceIPAddress'],
                        'UserAgent': json.loads(event['CloudTrailEvent'])['userAgent'],
                        'Region': json.loads(event['CloudTrailEvent'])['awsRegion'],
                        'ErrorCode': None,
                        'ErrorMessage': None
                    }

                    if 'errorCode' in json.loads(event['CloudTrailEvent']):
                        logdata['ErrorCode'] = json.loads(event['CloudTrailEvent'])['errorCode']

                    if 'errorMessage' in json.loads(event['CloudTrailEvent']):
                        logdata['ErrorMessage'] = json.loads(event['CloudTrailEvent'])['errorMessage']

                    loglist.append(logdata)

            printOutput(
                True,
                f"Found {len(loglist)} occurrences of {eventCombo} in logs",
                "success"
            )
            return loglist


        except Exception as e:
            printOutput(self.verbose, f"Error listing logs: {str(e)}", "failure")
            return []


