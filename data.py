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
    3: ["""
Good job! The next data types are the integer and the float.
Integers are normal numbers like 0, 1, -3 or 501239201849231849320.
Floats are floating-point numbers like 0.5, 3.3335 or -7.801.

They support maths!
`5 / 2` is 2.5
`5 * 3` is 15
`20 + 34` is 54
`2 - 80` is -78
`2 ** 3` is 8 (it is the times operator, equals 2 * 2 * 2)

Make the `output` be the square of `input` divided by 2 plus 1/4 of `input`.
        """,
        [[-10, 47.5], [0, 0], [3, 5.25], [5, 13.75]],
       ],
}
