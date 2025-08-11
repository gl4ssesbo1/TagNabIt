from core.Authentication.Authentication import authWithProfile
from core.Other.PrintOutput.PrintOutput import printOutput

from datetime import datetime

class EnumerateResources:
    def __init__(self, profile, verbose):
        self.verbose = verbose
        self.profile = profile
        self.tagClient = authWithProfile(
            Profile=self.profile,
            Service="resourcegroupstaggingapi"
        )
        self.ec2Client = authWithProfile(
            Profile=self.profile,
            Service="ec2"
        )

        self.ceClient = authWithProfile(
            Profile=self.profile,
            Service="ce"
        )

        self.lfClient = authWithProfile(
            Profile=self.profile,
            Service="lakeformation"
        )

        self.autoscalingClient = authWithProfile(
            Profile=self.profile,
            Service="autoscaling"
        )

        self.discoveryClient = authWithProfile(
            Profile=self.profile,
            Service="discovery"
        )

        self.redshiftClient = authWithProfile(
            Profile=self.profile,
            Service="redshift"
        )

    def enumerateResourcesUsingGetResources(self):
        try:
            resourcesReq = self.tagClient.get_resources()
            resources = resourcesReq['ResourceTagMappingList']
            while resourcesReq['PaginationToken'] != '':
                resourcesReq = self.tagClient.get_resources(PaginationToken=resourcesReq['PaginationToken'])
                resources.extend(resourcesReq['ResourceTagMappingList'])


            if len(resources) == 0:
                printOutput(
                    self.verbose,
                    f"No tags found using tag:GetResources",
                    "failure"
                )

            for resource in resources:
                printOutput(True, '-'*len(resource["ResourceARN"]), 'success')
                printOutput(True, f'  {resource["ResourceARN"]}', 'success')
                printOutput(True, '-'*len(resource["ResourceARN"]), 'success')


                if len(resource['Tags']) == 0:
                    printOutput(True, 'No Tags set to resource', 'loading')
                else:
                    printOutput(True, 'Tags', 'loading')
                    for tags in resource['Tags']:
                        print(f"\t[*] {tags['Key']}:{tags['Value']}")

        except Exception as e:
            printOutput(
                self.verbose,
                f"Error Trying to enumerate resources using tag:GetResources: {str(e)}",
                "failure"
            )

    def describeEC2Tags(self):
        try:
            resourcesReq = self.ec2Client.describe_tags()
            resources = resourcesReq["Tags"]
            while 'NextToken' in resourcesReq:
                resourcesReq = self.ec2Client.describe_tags(NextToken=resourcesReq['NextToken'])
                resources.extend(resourcesReq["Tags"])

            if len(resources) == 0:
                printOutput(
                    self.verbose,
                    f"No tags found using autoscaling:DescribeTags",
                    "failure"
                )

            for resource in resources:
                printOutput(True, '-'*len(resource["ResourceId"]), 'success')
                printOutput(True, f'  {resource["ResourceId"]}', 'success')
                printOutput(True, '-'*len(resource["ResourceId"]), 'success')

                printOutput(True, 'Tags', 'loading')
                print(f"\t[*] {resource['Key']}:{resource['Value']}")

        except Exception as e:
            printOutput(
                self.verbose,
                f"Error Trying to enumerate resources using ec2:DescribeTags: {str(e)}",
                "failure"
            )

    def describeCETags(self):
        try:
            now = datetime.now().strftime(
                "%Y-%m-%d"
            )

            resourcesReq = self.ceClient.get_tags(
                TimePeriod={
                    'Start': "2023-01-01",
                    'End': now
                }
            )

            resources = resourcesReq["Tags"]
            while 'NextPageToken' in resourcesReq:
                resourcesReq = self.ceClient.get_tags(NextToken=resourcesReq['NextPageToken'])
                resources.extend(resourcesReq["Tags"])

            if len(resources) == 0:
                printOutput(
                    self.verbose,
                    f"No tags found using ce:GetTags",
                    "failure"
                )

            for tag in resources:
                print(f"\t[*] {tag}")


        except Exception as e:
            printOutput(
                self.verbose,
                f"Error Trying to enumerate resources using ce:GetTags: {str(e)}",
                "failure"
            )

    def listLFTags(self):
        try:
            resourcesReq = self.lfClient.list_lf_tags()

            resources = resourcesReq["LFTags"]
            while 'NextToken' in resourcesReq:
                resourcesReq = self.lfClient.list_lf_tags(NextToken=resourcesReq['NextToken'])
                resources.extend(resourcesReq["LFTags"])

            if len(resources) == 0:
                printOutput(
                    self.verbose,
                    f"No tags found using lakeformation:ListLFTags",
                    "failure"
                )

            for resource in resources:
                printOutput(True, '-' * len(resource["CatalogId"]), 'success')
                printOutput(True, f'  {resource["CatalogId"]}', 'success')
                printOutput(True, '-' * len(resource["CatalogId"]), 'success')

                printOutput(True, f'TagKey: {resource["TagKey"]}', 'loading')

                if len(resource['TagValues']) == 0:
                    printOutput(True, 'No Tags set to resource', 'loading')
                else:
                    printOutput(True, 'Tags', 'loading')
                    for tags in resource['TagValues']:
                        print(f"\t[*] {tags['Value']}")


        except Exception as e:
            printOutput(
                self.verbose,
                f"Error Trying to enumerate resources using lakeformation:ListLFTags: {str(e)}",
                "failure"
            )

    def describeAutoscalingTags(self):
        try:
            resourcesReq = self.autoscalingClient.describe_tags()
            resources = resourcesReq["Tags"]
            while 'NextToken' in resourcesReq:
                resourcesReq = self.autoscalingClient.describe_tags(NextToken=resourcesReq['NextToken'])
                resources.extend(resourcesReq["Tags"])

            if len(resources) == 0:
                printOutput(
                    self.verbose,
                    f"No tags found using autoscaling:DescribeTags",
                    "failure"
                )


            for resource in resources:
                printOutput(True, '-'*(len(resource["ResourceId"])+len(resource["ResourceType"]) + 1), 'success')
                printOutput(True, f'  {resource["ResourceType"]}{resource["ResourceId"]}', 'success')
                printOutput(True, '-'*(len(resource["ResourceId"])+len(resource["ResourceType"]) + 1), 'success')

                printOutput(True, 'Tags', 'loading')
                print(f"\t[*] {resource['Key']}:{resource['Value']}")

        except Exception as e:
            printOutput(
                self.verbose,
                f"Error Trying to enumerate resources using autoscaling:DescribeTags: {str(e)}",
                "failure"
            )

    def describeDiscoveryTags(self):
        try:
            resourcesReq = self.discoveryClient.describe_tags()
            resources = resourcesReq["tags"]
            while 'nextToken' in resourcesReq:
                resourcesReq = self.discoveryClient.describe_tags(nextToken=resourcesReq['NextToken'])
                resources.extend(resourcesReq["tags"])

            if len(resources) == 0:
                printOutput(
                    self.verbose,
                    f"No tags found using discovery:DescribeTags",
                    "failure"
                )

            for resource in resources:
                printOutput(True, '-' * (len(resource["configurationId"]) + len(resource["configurationType"]) + 1),
                            'success')
                printOutput(True, f'  {resource["configurationType"]}{resource["configurationId"]}', 'success')
                printOutput(True, '-' * (len(resource["configurationId"]) + len(resource["configurationType"]) + 1),
                            'success')

                printOutput(True, f'timeOfCreation: {resource["timeOfCreation"]}', 'success')
                printOutput(True, 'Tags', 'loading')
                print(f"\t[*] {resource['key']}:{resource['value']}")

        except Exception as e:
            printOutput(
                self.verbose,
                f"Error Trying to enumerate resources using discovery:DescribeTags: {str(e)}",
                "failure"
            )

    def describeRedshiftTags(self):
        try:
            resourcesReq = self.redshiftClient.describe_tags()
            resources = resourcesReq["TaggedResources"]
            if 'Marker' in resourcesReq:
                while resourcesReq['Marker'] == "":
                    resourcesReq = self.redshiftClient.describe_tags(nextToken=resourcesReq['Marker'])
                    resources.extend(resourcesReq["TaggedResources"])

            if len(resources) == 0:
                printOutput(
                    self.verbose,
                    f"No tags found using redshift:DescribeTags",
                    "failure"
                )

            for resource in resources:
                printOutput(True, '-' * (len(resource["ResourceName"]) + len(resource["ResourceType"]) + 1),
                            'success')
                printOutput(True, f'  {resource["ResourceType"]}{resource["ResourceName"]}', 'success')
                printOutput(True, '-' * (len(resource["ResourceType"]) + len(resource["ResourceName"]) + 1),
                            'success')

                printOutput(True, 'Tags', 'loading')
                print(f"\t[*] {resource['Tag']['Key']}:{resource['Tag']['Value']}")

        except Exception as e:
            printOutput(
                self.verbose,
                f"Error Trying to enumerate resources using discovery:DescribeTags: {str(e)}",
                "failure"
            )