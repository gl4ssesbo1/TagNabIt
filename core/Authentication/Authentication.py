import boto3

from core.Other.PrintOutput.PrintOutput import printOutput


def authWithProfile(Profile, Service):
    try:
        session = boto3.Session(
            profile_name=Profile
        )

        return session.client(Service)
    except Exception as e:
        printOutput(True, f"Error creating Client: {str(e)}", 'failure')


def authenticate(Profile=None, Service=None):
    return authWithProfile(Profile=Profile, Service=Service)

