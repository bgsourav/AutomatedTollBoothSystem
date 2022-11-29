
import re
from pprint import pprint
import inquirer  


def digits_validation(answers, current):
    if not re.match("^[0-9]{6}$", current):
        raise inquirer.errors.ValidationError("", reason="Invalid format!")
    return True

questions = [
    inquirer.Text("Number",message="Enter number",validate=phone_validation)
]
answers = inquirer.prompt(questions)
pprint(answers)
