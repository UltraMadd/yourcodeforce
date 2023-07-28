from dataclasses import dataclass
import re
import argparse
from typing import Callable, Dict
import sys
from consts import *



@dataclass
class Problem:
    number: int
    description: str
    answer: str
    
    @classmethod
    def from_raw(cls, raw: str):
        raw_splitted = re.split(NUMBER_PROBLEM_DEL_REGEX, raw)
        number = int(raw_splitted[0])
        description, answer = raw_splitted[1].split("Answer: ")
        answer = answer.strip()
        description = "\n".join(map(lambda s: s.removeprefix(' ' * 3), description.split("\n")))
        return cls(number, description, answer)

@dataclass
class Config:
    action: str
    options: Dict[str, str]


def prompt_for_yes_no(question: str, max_attempts: int = 3) -> bool:
    for _ in range(max_attempts):
        answer = input(question)
        if answer.lower() in ("y", "yes"):
            return True
        elif answer.lower() in ("n", "no"):
            return False
    raise ValueError("Too many attempts to answer on a simple yes/no question. You're dumb?")

def prompt_for_number(validator: Callable[[int], bool], prompt: str = "Enter a number: ", hint: str = "Wrong number", max_attempts: int = 3) -> int:
    for _ in range(max_attempts):
        try:
            number = int(input(prompt))
        except ValueError:
            print(hint)
            continue
        if validator(number):
            return number
    raise ValueError("Too many attempts to enter a number")

def new():
    pass

def eul(eul_name: str = "euler.txt") -> None:
    """
    Problems from Project Euler
    :param eul_name: file name with problems to read from
    :type eul_name: str
    """
    problems = []
    with open(eul_name) as file:
        content = file.read()
        problems = content.split("\nProblem ")
        problems = list(map(Problem.from_raw, problems[1:]))
        problem_n = problems[-1].number
        problem_number = prompt_for_number(
                lambda n: n in range(1, problem_n + 1),
                max_attempts=10, 
                prompt="Enter a problem number [1, %s]: " % problem_n
                )
        problem = problems[problem_number - 1]
        print(PROBLEM_FORMAT % (problem_number, problem.description))
        if prompt_for_yes_no("Do you wan to create file problem_%s.py with test cases for this problem y(es)/n(o)?: " % problem_number):
            with open("problem_%s.py" % problem_number, "w") as file:
                file.write(PY_TESTCASE_FORMAT % (problem.number, problem.description, problem.answer))
        if not prompt_for_yes_no("Do you wan to create file problem_%s.c with test cases for this problem y(es)/n(o)?: " % problem_number):
            return
        with open("problem_%s.c" % problem_number, "w") as file:
            file.write(C_TESTCASE_FORMAT % (problem.number, problem.description, problem.answer))



def usage():
    print("Usage: python %s <eul|new> [options]" % sys.argv[0])

def cli():
    argv = sys.argv
    if len(argv) < 2:
        usage()
        return
    if argv[1] == 'eul':
        if len(argv) == 3:
            eul(argv[2])
        else:
            eul()
    elif argv[1] == 'new':
        new()
    else:
        usage()


def main():
    cli()

if __name__ == "__main__":
    main()
