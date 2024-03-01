import re
import sys
from sys import argv
from dataclasses import dataclass
from typing import Optional

from ycf.consts import (
    C_TESTCASE_FORMAT,
    PY_TESTCASE_FORMAT,
    DO_YOU_WANT_TESTCAES,
    PROBLEM,
    PROBLEM_FORMAT,
)

NUMBER_PROBLEM_DEL_REGEX = re.compile("\n=+\n")


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


def errprint(message: str):
    print("ERROR:")
    print(message, file=sys.stderr)
    sys.exit(1)


def prompt_for_yes_no(prompt: str, max_attempts: int = 10) -> bool:
    for _ in range(max_attempts):
        answer = input(prompt)
        if answer.lower() in ("y", "yes"):
            return True
        if answer.lower() in ("n", "no"):
            return False
    errprint("Too many attempts to answer on a simple yes/no question. You're dumb?")
    return False


def prompt_for_number(
    in_range: Optional[range],
    prompt: str,
    max_attempts: int = 10,
) -> Optional[int]:
    for _ in range(max_attempts):
        try:
            number = int(input(prompt))
        except ValueError:
            continue
        if in_range is None or number in in_range:
            return number
    errprint("Too many attempts to enter a number")
    return None


def eul(eul_name: str = "euler.txt") -> None:
    problems = []
    with open(eul_name) as test_file:
        problems = test_file.read().split("\nProblem ")
        problems = [Problem.from_raw(problem) for problem in problems[1:]]
        problem_len = problems[-1].number

        problem_number = prompt_for_number(
            in_range=range(1, problem_len + 1),
            prompt=f"Enter a problem number [1, {problem_len}]: "
        )
        if problem_number is None:
            raise ValueError("Wrong problem number")

        problem = problems[problem_number - 1]
        print(PROBLEM_FORMAT % (problem_number, problem.description))

        test_files = [("py", PY_TESTCASE_FORMAT), ("c", C_TESTCASE_FORMAT)]
        for test_file_ext, test_file_format in test_files:
            test_file_name = PROBLEM % (problem_number, test_file_ext)
            if prompt_for_yes_no(DO_YOU_WANT_TESTCAES % test_file_name):
                with open(test_file_name, "w") as test_file:
                    test_file.write(
                        test_file_format
                        % (problem.number, problem.description, problem.answer)
                    )


def usage():
    print("Usage: %s <eul|help> [options]" % sys.argv[0])


def list_commands():
    print("Available commands:\n"\
          "eul: Euler")


def print_help():
    usage()
    list_commands()


def cli():
    if len(argv) < 2:
        usage()
        return
    if argv[1] == "eul":
        if len(argv) == 3:
            eul(argv[2])
        else:
            eul()
    elif argv[1] == "help":
        print_help()
    else:
        usage()


def main():
    cli()


if __name__ == "__main__":
    main()
