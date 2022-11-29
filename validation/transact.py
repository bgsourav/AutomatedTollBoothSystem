import re
from pprint import pprint
import inquirer  


print('Transaction ID must TR followed by three correct numbers')
def transaction_validation(answers, current):
    if not re.match("TR[0-9]{6}$",current):
        raise inquirer.errors.ValidationError("", reason="Invalid transaction ID input!")
    return True

questions = [
    inquirer.Text("Transaction ID",message="Enter transaction ID",validate=transaction_validation)
]
answers = inquirer.prompt(questions)
pprint(answers)
