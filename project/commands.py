"""
    Author: Duodu Randy
    Project: Personal Assistant
    Description: A speech and text recognition program for experimental purposes.
    Date Created: Tuesday, 6th October, 2020
    Tech Stacks: Python
    Topics Learnt: Git
"""

# Standard library imports


# Related third party imports


# Local application/library specific imports
"""
    Author: Duodu Randy
    Project: Personal Assistant
    Description: A speech and text recognition program for experimental purposes.
    Date Created: Tuesday, 6th October, 2020
    Tech Stacks: Python
    Topics Learnt: Git
"""

# Standard library imports


# Related third party imports


# Local application/library specific imports
"""
    Author: Duodu Randy
    Project: Personal Assistant
    Description: A speech and text recognition program for experimental purposes.
    Date Created: Tuesday, 6th October, 2020
    Tech Stacks: Python
    Topics Learnt: Git
"""

# Standard library imports


# Related third party imports


# Local application/library specific imports

# Local modules
import os
from pathlib import Path
import subprocess
import shlex

# User-defined modules


# Third-party modules

   

home = Path.home()
# bashCom = str("ps aux | awk '{ for(i=1;i<=NF;i++) {if ( i >= 11 ) printf $i' '}; printf '\n' }' | grep code | grep personal_assistant")
bashCom = f"ps axu"
# bashCom = f"ls -ll"
process = subprocess.Popen(shlex.split(bashCom),
stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)


working_trees = []
for output in process.stdout.readlines():
    project_name = 'personal_assistant'
    if ('code' or 'pycharm' or 'gedit') and ('personal_assistant' or 'auth0') in output:
        sd = output.split("/home")[-1]
        working_trees.append(f"/home{sd}".strip('\n'))

print(f"Output: {working_trees}")

msg = "testing app"
commit_command = f"git commit -m {msg.replace(' ', '_')}"
for working_tree in working_trees:
    subprocess.Popen(shlex.split("git add ."),
    stdout=subprocess.PIPE,universal_newlines=True, 
    cwd=working_tree)

    process_two = subprocess.Popen(shlex.split(commit_command),
    stdout=subprocess.PIPE,universal_newlines=True, 
    cwd=working_tree)

    output, _ = process_two.communicate()
    print('Git info', output)



















    