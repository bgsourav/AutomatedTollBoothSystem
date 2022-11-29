import re
from pprint import pprint
import inquirer  


print('Vehicle Number should conform to Indian registration standards')
def vehicle_validation(answers, current):
    if not re.match("^[A-Z]{2}[ -][0-9]{1,2}(?: [A-Z])?(?: [A-Z]*)? [0-9]{4}$",current):
        raise inquirer.errors.ValidationError("", reason="Invalid vehicle number input format!")
    return True

questions = [
    inquirer.Text("Vehicle Registration Number",message="Enter vehicle registration number",validate=vehicle_validation)
]
answers = inquirer.prompt(questions)
pprint(answers)