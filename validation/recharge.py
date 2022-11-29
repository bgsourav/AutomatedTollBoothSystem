import re
from pprint import pprint
import inquirer  

def recharge_validation(answers, current):

    if not re.match("^\d{1,10}$", current):
        raise inquirer.errors.ValidationError("", reason="Invalid format!")
    return True

questions = [
    inquirer.Text("Recharge",message="Enter recharge",validate=recharge_validation)
]
answers = inquirer.prompt(questions)
pprint(answers)