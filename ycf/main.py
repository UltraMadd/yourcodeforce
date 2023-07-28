from dataclasses import dataclass
from typing import TypeVar
import re
import argparse
from typing import Callable, Dict, Optional
import sys
from ycf.consts import *


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
        description = "\n".join(
            map(lambda s: s.removeprefix(" " * 3), description.split("\n"))
        )
        return cls(number, description, answer)


@dataclass
class Config:
    action: str
    options: Dict[str, str]


def errprint(s: str):
    print("ERROR:")
    print(s, file=sys.stderr)
    exit(1)


def prompt_for_yes_no(question: str, max_attempts: int = 3) -> bool:
    for _ in range(max_attempts):
        answer = input(question)
        if answer.lower() in ("y", "yes"):
            return True
        elif answer.lower() in ("n", "no"):
            return False
    errprint("Too many attempts to answer on a simple yes/no question. You're dumb?")
    return False


def prompt_for_number(
    in_range: Optional[range],
    prompt: str = "Enter a number: ",
    hint: str = "Wrong number",
    max_attempts: int = 3,
) -> int:
    for _ in range(max_attempts):
        try:
            number = int(input(prompt))
        except ValueError:
            print(hint)
            continue
        if in_range is not None and number in in_range:
            return number
    errprint("Too many attempts to enter a number")
    return -1


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
            range(1, problem_n + 1),
            max_attempts=10,
            prompt="Enter a problem number [1, %s]: " % problem_n,
        )
        if problem_number is None:
            raise ValueError("Wrong problem number")
        problem = problems[problem_number - 1]
        print(PROBLEM_FORMAT % (problem_number, problem.description))
        test_files = [("py", PY_TESTCASE_FORMAT), ("c", C_TESTCASE_FORMAT)]
        for test_file_ext, test_file_format in test_files:
            test_file_name = PROBLEM % (problem_number, test_file_ext)
            if prompt_for_yes_no(DO_YOU_WANT_TESTCAES % test_file_name):
                with open(test_file_name, "w") as file:
                    file.write(
                        test_file_format
                        % (problem.number, problem.description, problem.answer)
                    )


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
    if argv[1] == "eul":
        if len(argv) == 3:
            eul(argv[2])
        else:
            eul()
    elif argv[1] == "new":
        new()
    elif argv[1] == "help":
        help()
    else:
        usage()


def main():
    cli()


if __name__ == "__main__":
    main()
