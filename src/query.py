# This module converts the raw query to postfix expression
# based on the standard precedence order.


boolean_ops = ["and","or","not"]
precendence = {
    'not': 3,
    'and': 2,
    'or': 1,
}


def to_postfix(infix_tokens):
    postfix = []
    stack = []
    for i, word in enumerate(infix_tokens):
        if word in boolean_ops:
            while len(stack) != 0 and precendence[word] < precendence[stack[-1]]:
                postfix.append(stack[-1])
                stack.pop()

            stack.append(word)

        else:
            postfix.append(word)

    while len(stack) > 0:
        postfix.append(stack[-1])
        stack.pop()

    print(postfix)
    return postfix

