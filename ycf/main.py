from dataclasses import dataclass
from typing import TypeVar
import re
import argparse
from typing import Callable, Dict, Optional
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


V = TypeVar("V")
def prompt_for_valid(
        validator: Callable[[str], Optional[V]],
        on_invalid: Callable,
        prompter: Callable[[], str],
        max_attempts: int = 3
        ) -> Optional[V]:
    for _ in range(max_attempts):
        prompted = validator(prompter())
        if prompted is not None:
            on_invalid()
        else:
            return prompted

def errprint(s: str):
    print("ERROR:")
    print(s, file=sys.stderr)
    exit(1)

def yes_or_no(s: str) -> Optional[bool]:
    if s.lower() == ("y", "yes"):
        return True
    if s.lower() in ("n", "no"):
        return False
    return None

def prompt_for_yes_no(question: str, max_attempts: int = 3) -> bool:
    prompted = prompt_for_valid(
            validator=yes_or_no,
            on_invalid=lambda: print("Please, answer: y(es) or n(o)"),
            prompter=lambda: input("%s [y/n]: " % question),
            max_attempts=max_attempts
            )
    if prompted:
        return prompted
    errprint("Wrong answer")
    return False

def to_number(s: str) -> Optional[int]:
    try:
        return int(s)
    except ValueError:
        pass

def valid_num(validator: Callable, n: Optional[int]) -> Optional[int]:
    if n is None:
        return None
    return validator(n)


def prompt_for_number(
        validator: Callable[[int], Optional[int]], 
        prompt: str = "Enter a number: ", 
        hint: str = "Wrong number", 
        max_attempts: int = 3
        ) -> Optional[int]:
    prompted = prompt_for_valid(
            validator=lambda x: valid_num(validator, to_number(x)),
            on_invalid=lambda: print(hint),
            prompter=lambda: input(prompt),
            max_attempts=max_attempts
            )
    if prompted:
        return prompted
    errprint("Wrong answer")

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
        if problem_number is None:
            raise ValueError("Wrong problem number")
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
    print("Usage: python %s <eul|new|help> [options]" % sys.argv[0])

def list_commands():
    print("Available commands:")
    print("eul: Euler")
    print("new: WIP")

def help():
    usage()
    list_commands()

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
    elif argv[1] == 'help':
        help()
    else:
        usage()


def main():
    cli()

if __name__ == "__main__":
    main()
