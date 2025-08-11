import json
import os
import prettytable
from core.Other.PrintOutput.PrintOutput import printOutput
from termcolor import colored

class TablePrint():
    def logsTablePrint(self, queryResult, verbose):
        typeLength = 0
        nameLength = 0
        allowLength = 0
        fieldNames = [
            'EventTime',
            'EventName',
            'Username',
            'AccessKeyId',
            'AccountID',
            'ErrorCode',
            'ErrorMessage'
        ]

        if len(queryResult) == 0:
            printOutput(verbose,
                "No values for this query",
                "success"
            )

        else:
            # print(tabulate(queryResult, headers='keys', tablefmt='psql'))
            column_width, row_width = os.get_terminal_size(0)
            maxwidth = int(os.get_terminal_size().columns / 3)
            table = prettytable.PrettyTable(
                max_table_width=column_width,
                align='l',
                field_names=fieldNames,
                max_width=maxwidth
            )
            table.set_style(prettytable.DOUBLE_BORDER)
            for row in queryResult:
                table.add_row(row.values())
                #table.add_row(["="*typeLength, "="*nameLength, "="*allowLength])

            print(table)
        printOutput(verbose, '-' * (os.get_terminal_size().columns - 10), "success")

    def policyTableprint(self, queryResult, verbose):
        allfields = []

        versionLength = len("PolicyVersion")
        attachcountLength = len("PolicyAttachmentCount")
        nameLength = len("PolicyName")
        allowLength = len("Allow")

        for identity in queryResult:
            fieldNames = identity

            if fieldNames['Allowed']:
                fieldNames['Allowed'] = colored(u'    \u2713    ', "green")
            else:
                fieldNames['Allowed'] = colored(u"    \u2717    ", "red")

            if len(fieldNames['PolicyName']) > nameLength:
                nameLength = len(fieldNames['PolicyName'])

            if len(fieldNames['Allowed']) > allowLength:
                allowLength = len(fieldNames['Allowed'])

            del(fieldNames['PolicyDocument'])

            allfields.append(fieldNames)

        if len(allfields) == 0:
            printOutput(verbose,
                "No values for this query",
                "success"
            )

        else:
            # print(tabulate(queryResult, headers='keys', tablefmt='psql'))
            column_width, row_width = os.get_terminal_size(0)
            maxwidth = int(os.get_terminal_size().columns / 3)
            table = prettytable.PrettyTable(
                max_table_width=column_width,
                align='l',
                field_names=["PolicyName", "PolicyVersion", "PolicyAttachmentCount", "Allowed"],
                #max_width=maxwidth
            )
            table.set_style(prettytable.DOUBLE_BORDER)
            for row in allfields:
                table.add_row(row.values())
                table.add_row(["-"*nameLength, "-"*versionLength, "-"*attachcountLength, "-"*allowLength])

            print(table)
        printOutput(verbose, '-' * (os.get_terminal_size().columns - 10), "success")


    def listToString(self, theList):
        stringReturn = ""
        for field in theList:
            stringReturn += field + '\n'

        return stringReturn

    def tableprint(self, queryResult, verbose, fields):
        allfields = []

        fieldLengths = {

        }

        for field in fields:
            fieldLengths[field] = '-' * len(field)

        for fieldNames in queryResult:
            rowData = {}

            for name, value in fieldNames.items():
                if name in fields:
                    if type(value) == list:
                        for line in value:
                            if len(line) > len(fieldLengths[name]):
                                fieldLengths[name] = '-' * len(line)

                        value = self.listToString(value)

                    else:
                        if type(value) != str:
                            value = str(value)
                        if len(value) > len(fieldLengths[name]):
                            fieldLengths[name] = '-' * len(value)

                    rowData[name] = value

            allfields.append(rowData)

        if len(allfields) == 0:
            printOutput(verbose,
                "No values for this query",
                "success"
            )

        else:
            # print(tabulate(queryResult, headers='keys', tablefmt='psql'))
            column_width, row_width = os.get_terminal_size(0)
            maxwidth = int(os.get_terminal_size().columns / 2)
            table = prettytable.PrettyTable(
                max_table_width=column_width,
                align='l',
                field_names=fields,
                max_width=maxwidth
            )
            table.set_style(prettytable.DOUBLE_BORDER)
            for row in allfields:
                table.add_row(row.values())
                table.add_row(fieldLengths.values())

            print(table)
        printOutput(verbose, '-' * (os.get_terminal_size().columns - 10), "success")

    def tableprintold(self, queryResult, verbose):
        allfields = []

        typeLength = 0
        nameLength = 0
        allowLength = 0
        polnameLength = 0

        for identity in queryResult:
            fieldNames = identity

            if fieldNames['Allowed']:
                fieldNames['Allowed'] = colored(u'    \u2713    ', "green")
            else:
                fieldNames['Allowed'] = colored(u"    \u2717    ", "red")

            if len(fieldNames['Type']) > typeLength:
                typeLength = len(fieldNames['Type'])

            if len(fieldNames['Name']) > nameLength:
                nameLength = len(fieldNames['Name'])

            if len(fieldNames['Allowed']) > allowLength:
                allowLength = len(fieldNames['Allowed'])

            if len(fieldNames['PolicyNames']) > polnameLength:
                polnameLength = len(fieldNames['PolicyNames'])


            allfields.append(fieldNames)

        if len(allfields) == 0:
            printOutput(verbose,
                "No values for this query",
                "success"
            )

        else:
            # print(tabulate(queryResult, headers='keys', tablefmt='psql'))
            column_width, row_width = os.get_terminal_size(0)
            maxwidth = int(os.get_terminal_size().columns / 3)
            table = prettytable.PrettyTable(
                max_table_width=column_width,
                align='l',
                field_names=["Type", "Name", "Allowed", "PolicyNames"],
                max_width=maxwidth
            )
            table.set_style(prettytable.DOUBLE_BORDER)
            for row in allfields:
                table.add_row(row.values())
                table.add_row(["="*typeLength, "="*nameLength, "="*allowLength, "="*polnameLength])

            print(table)
        printOutput(verbose, '-' * (os.get_terminal_size().columns - 10), "success")