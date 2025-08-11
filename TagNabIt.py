import os

from core.Other.Arguments.ArgParse import parseArgs
from core.Other.PrintOutput.PrintOutput import printOutput
from core.Authentication.Authentication import authWithProfile
from core.Resources.MainActivity.MainActivity import MainActivity

args = parseArgs()

if not os.path.exists("./output"):
    os.mkdir("./output")

profile = args.profile
accountid = None

try:
    client = authWithProfile(Profile=profile, Service="sts")
    if client is None:
        exit()

    accountid = client.get_caller_identity()['Account']
    printOutput(True, f"Testing Account {accountid}", "loading")

except Exception as e:
    printOutput(True, f"Error with credentials provided: {str(e)}", "error")
    exit()

if accountid is None:
    printOutput(True, f"Error with credentials provided", "error")
    exit()

if not os.path.exists(f'./output/{accountid}'):
    os.mkdir(f"./output/{accountid}")

try:
    policyscope = args.scope
except:
    policyscope = None

#mainactivity = MainActivity(profile=profile, accountID=accountid, verbose=args.verbose, command=args.command, args=args, policyscope=policyscope)
mainactivity = MainActivity(
    profile=profile,
    accountID=accountid,
    command=args.command,
    args=args
)
mainactivity.main_activity()

