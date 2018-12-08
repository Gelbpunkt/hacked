msg = """
Welcome to hacked.!
This is a Discord Bot to teach people how to program.
You do so by finishing levels with tasks.
Type `///start` to start (you figured it out)
Type `///task` to view your current task
Type `///solve` to solve your current task in a code-style.

e.g.
```
///solve
\u200b`\u200b`\u200b`js
say("Hello World!");
\u200b`\u200b`\u200b`
```

Every task has an input (in code referenced to as simply `input` and you have to generate output by making a variable called output.
Example:
This code has the task to return the first letter of the input.
```
///solve
\u200b`\u200b`\u200b`js
say(input); // just to see what the input is, you can skip this
output = input[0]; // the first letter is the output now and it will be tested against a few values!
\u200b`\u200b`\u200b`
```
"""

levels = {
    1: ["""
Let's get started. At the end of every line not ending with a `{` or `}`, add a `;`.
Assign variables by using `variableName = variableValue;`.
Variables are like a placeholder for something, they hold the value assigned until you change it.
Your first task is to make our `output` variable 1. That's it!
Type `///solve {codeblock}` to solve the task!
        """,
        [[0, 1], [1, 1], [2, 1]], # data to test it against (in, out)
       ],
    2: ["""
Well done! Now, there are some data types you should know.
First of all, the boolean.
Booleans are either `true` or `false`.
You can either do `a = true;` or compare using `>, >=, <, <=, ==, !=`.

`>`: Greater than (`a > b`)
`>=`: Greater than or equal (`a >= b`)
`<`: Smaller than (`a < b`)
`<=`: Smaller than or equal (`a <= b`))
`==`: Equals (`a == b`)
`!=`: Unequal (`a != b`)

This means you can do
`a = 2 > 1;`
and a will be true.

Your task is to make `output` show whether `input` is equal to 1 or not.
        """,
        [[0, False], [1, True], [2, False]],
       ],
}
