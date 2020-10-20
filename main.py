"""
    Author: Duodu Randy
    Project: Personal Assistant
    Description: A speech and text recognition program for experimental purposes.
    Date Created: Tuesday, 6th October, 2020
    Tech Stacks: Python
    Topics Learnt: Git
"""

# Standard library imports
import datetime

# Related third party imports


# Local application/library specific imports
from project import message

# Synchronous version done in 11.68 seconds.
if __name__ == "__main__":
    t0 = datetime.datetime.now()
    print(message.version())
    dt = datetime.datetime.now() - t0
    print("Synchronous version done in {:,.2f} seconds.".format(dt.total_seconds()))
