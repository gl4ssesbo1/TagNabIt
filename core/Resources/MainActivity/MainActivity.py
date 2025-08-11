import os.path

from core.Other.PrintOutput.PrintOutput import printOutput
from core.Other.TablePrint import TablePrint
from core.Resources.CloudTrail.CheckUsage import CheckUsage
from core.Resources.Tags.BruteforceResources import BruteforceResources
from core.Resources.Tags.EnumerateResources import EnumerateResources
from core.Resources.Tags.BruteforceIAM import BruteforceIAM

import json
from core.Authentication.Authentication import authWithProfile
from core.Resources.OutputDump.OutputDump import dumpCSV, loadCSV
from alive_progress import alive_bar

class MainActivity:
    def __init__ (self, profile, accountID, command, args):#(self, profile, accountID, verbose, command, args, policyscope):
        #self.args.verbose = verbose
        self.args = args
        #self.UserCheckObj = UserCheck(profile=profile, verbose=self.args.verbose)
        #self.RoleCheckObj = RoleCheck(profile=profile, verbose=self.args.verbose)
        self.profile = profile
        self.accountID = accountID
        self.command = command
        #self.args = args
        self.tablePrintObj = TablePrint()

    def main_activity(self):
        if self.command == "CHECKUSAGE":
            printOutput(True, f"Finding Occurrences of Tag Based Enumeration in Cloud", 'loading')
            self.check_usage()

        elif self.command == "BRUTEFORCERESOURCES":
            printOutput(True, f"Bruteforcing AWS Resources for service {self.args.service}", 'loading')
            self.bruteforceAWSResources()

        elif self.command == "BRUTEFORCEIAM":
            printOutput(True, f"Bruteforcing IAM {self.args.resource_type}s", 'loading')
            self.bruteforceIAM()

        elif self.command == "ENUMERATERESOURCES":
            printOutput(True, f"Enumerating AWS Resources using tag:GetResources", 'loading')
            self.enumerateResourcesUsingGetResources()

    def check_usage(self):
        check_usage = CheckUsage(
            profile=self.profile,
            verbose=self.args.verbose,
            accountID=self.accountID
        )
        check_usage.check_usage()

    def enumerateResourcesUsingGetResources(self):
        enumerateResources = EnumerateResources(
            profile=self.profile,
            verbose=self.args.verbose
        )
        printOutput(True, '------------------------------------------------------------', 'success')
        printOutput(True, f'  Enumerate using tag:GetResources', 'success')
        printOutput(True, '------------------------------------------------------------', 'success')
        enumerateResources.enumerateResourcesUsingGetResources()
        print()
        print()

        printOutput(True, '------------------------------------------------------------', 'success')
        printOutput(True, f'  Enumerate using ec2:DescribeTags', 'success')
        printOutput(True, '------------------------------------------------------------', 'success')
        enumerateResources.describeEC2Tags()
        print()
        print()

        printOutput(True, '------------------------------------------------------------', 'success')
        printOutput(True, f'  Enumerate using ce:GetTags', 'success')
        printOutput(True, '------------------------------------------------------------', 'success')
        enumerateResources.describeCETags()
        print()
        print()

        printOutput(True, '------------------------------------------------------------', 'success')
        printOutput(True, f'  Enumerate using lakeformation:ListLFTags', 'success')
        printOutput(True, '------------------------------------------------------------', 'success')
        enumerateResources.listLFTags()
        print()
        print()

        printOutput(True, '------------------------------------------------------------', 'success')
        printOutput(True, f'  Enumerate using autoscaling:DescribeTags', 'success')
        printOutput(True, '------------------------------------------------------------', 'success')
        enumerateResources.describeAutoscalingTags()
        print()
        print()

        printOutput(True, '------------------------------------------------------------', 'success')
        printOutput(True, f'  Enumerate using discovery:DescribeTags', 'success')
        printOutput(True, '------------------------------------------------------------', 'success')
        enumerateResources.describeDiscoveryTags()
        print()
        print()

        printOutput(True, '------------------------------------------------------------', 'success')
        printOutput(True, f'  Enumerate using redshift:DescribeTags', 'success')
        printOutput(True, '------------------------------------------------------------', 'success')
        enumerateResources.describeRedshiftTags()
        print()
        print()



    def bruteforceAWSResources(self):
        bruteforceresources = BruteforceResources(
            profile=self.profile,
            resourceARNsFile=self.args.resource_arn_file,
            service=self.args.service
        )
        bruteforceresources.bruteforceTask()

    def bruteforceIAM(self):
        bruteforceIAMObj = BruteforceIAM(
            profile=self.profile,
            resourceARNsFile=self.args.resource_file,
            resourceType=self.args.resource_type,
            accountID=self.accountID,
            region=self.args.region
        )
        bruteforceIAMObj.bruteforceIAMMain()