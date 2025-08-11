from termcolor import colored

def printOutput(verbose, message, type):
    if type == "failure":
        print(
            colored(
                f"[*] {message}!", "red", attrs=['bold']
            )
        )
    elif type == "loading":
        if verbose:
            print(
                colored(
                    f"[*] {message}...", "yellow", attrs=['bold']
                )
            )
    elif type == "success":
        print(
            colored(
                f"[*] {message}!", "green", attrs=['bold']
            )
        )

