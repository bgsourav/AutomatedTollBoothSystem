import re
from pprint import pprint
import inquirer  

#Bank account number has a minimum of 9 numbers and a maximum of 18 numbers
print('Bank Account number should conform to RBI standards')
def account_validation(answers, current):
    if not re.match("^\d{9,18}$",current):
        raise inquirer.errors.ValidationError("", reason="Invalid account number input format!")
    return True

questions = [
    inquirer.Text("Account Number",message="Enter account number",validate=account_validation)
]
answers = inquirer.prompt(questions)
pprint(answers)