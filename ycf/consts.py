import re


NUMBER_PROBLEM_DEL_REGEX = re.compile("\n=+\n")
PROBLEM_FORMAT = """
Problem #%s
<->

%s

<->
"""

with open("./md5.c") as md5dcl:
    MD5DECL = md5dcl.read()

C_TESTCASE_FORMAT = """\
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>


// %s
/* %s */
void md5String(char *input, uint8_t *result);

char *solve() {
        return "";  // TODO solve
}

int main(int argc, char **argv) {
        uint8_t out[16];
        char out_str[33];
        out_str[32] = '\\0';
        md5String(solve(), out);
        for (int i = 0; i < 16; i++) {
                sprintf(out_str + i*2, "%%02x", out[i]);
        }
        if (strcmp("%s", out_str)) {
                printf("Wrong answer\\n");
        } else {
                printf("You get it right!\\n");
        }
}

""" + MD5DECL.replace("%", "%%")
PY_TESTCASE_FORMAT = """\
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


