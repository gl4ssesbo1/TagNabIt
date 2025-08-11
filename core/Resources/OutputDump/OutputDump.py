import csv, json
from core.Other.PrintOutput.PrintOutput import printOutput
import pandas as pd

def dumpCSV(result, outputdir, outputfile, headers):
    try:
        csvfile = csv.writer(open(f'./output/{outputdir}/{outputfile}.csv', "w"))
        csvfile.writerow(headers)
        for row in result:
            csvfile.writerow(row.values())
        return True

    except Exception as e:
        printOutput(True, f"Error outputting to ./output/{outputdir}/{outputfile}.csv: {str(e)}", "failure")
        return False

def loadCSV(csvFilePath):
    try:
        df = pd.read_csv(csvFilePath)
        return json.loads(df.to_json(orient="records"))

    except Exception as e:
        printOutput(True, f"Error loading file {csvFilePath} contents: {str(e)}", "failure")
        return None

