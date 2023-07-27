from dataclasses import dataclass
import re
from typing import Callable
import sys


NUMBER_PROBLEM_DEL_REGEX = re.compile("\n=+\n")
PROBLEM_FORMAT = """
Problem #%s
<->

%s

<->
"""
TESTCASE_FORMAT = """\
# %d
'''
%s
'''
from hashlib import md5 as _test_md5_hash

WRONG_ANSWER_MSG = "Wrong answer. Got: UNHASHED: %%s, HASHED: %%s, expected: HASHED: %%s. (in md5 hash, so that is not an answer)"
ANSWER = "%s"

def solve() -> str:
    ...  # TODO solve

def test():
    ret = solve()
    assert isinstance(ret, str)
    hashed = _test_md5_hash(ret.encode()).hexdigest()
    assert hashed == ANSWER, WRONG_ANSWER_MSG %% (ret, hashed, ANSWER)
    print('''Tests passed. 
          You're good to go. 
          Good luck! 
          Congratulations! 
          Wow that's a lot of problems! 
          You're a genius! 
          You're a genius! 
          I love you!
                                                    - AI generated.''')

if __name__ == "__main__":
    test()
"""


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
        problem_number = prompt_for_number(lambda n: n in range(1, problem_n + 1), max_attempts=10, prompt="Enter a problem number [1, %s]: " % problem_n)
        problem = problems[problem_number - 1]
        print(PROBLEM_FORMAT % (problem_number, problem.description))
        if not prompt_for_yes_no("Do you wan to create file problem_%s.py with test cases for this problem y(es)/n(o)?: " % problem_number):
            return
        with open("problem_%s.py" % problem_number, "w") as file:
            file.write(TESTCASE_FORMAT % (problem.number, problem.description, problem.answer))

def usage():
    print("Usage: python %s <eul|new> [options]" % sys.argv[0])

def main():
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

if __name__ == "__main__":
    main()
