# JavaScript for Python developers

---

# Comparison

```python
# Python
words = ["I", "love", "programming"]
for word in words:
  print(word)
```

```js
// JavaScript
const words = ["I", "love", "programming"]
for (let word of words) {
  console.log(word)
}
```

---

# Declaring variables

The first time you use a variable, you _declare_ it using `let` or `const`.

```js
const names = ["Blake", "Marion", "Keelan"]
let currentUser = "Blake"
```

---

# What if I forget to use `let` or `const`?

- The variable ends up being in the global scope
- Everything breaks
- You get confused

---

# Naming

In JavaScript, use `camelCase` instead of `snake_case`.

---

# Curly braces

Pretty much everywhere Python uses indentation, JavaScript uses curly braces.

```js
if (test) {
  runCode()
}

function doIt() {
  console.log("do it!")
}

for (let word of words) {
  console.log(word)
}
```

---

# Data types

- boolean (`true` and `false` -- no caps)
- number
- string
- `null` -- like `None`
- `undefined`

---

# Strings

- No `"""`
- Instead of f-strings, we have _template literals_

```python
greeting = f"Hello, {person}!" # Python
```

```js
let greeting = `Hello, ${person}!` // JavaScript
```

---

# Data structures

- _array_ - like a list
- _object_ - like a dict, but kind of like a Python object
- _Map_ - like a dict, but not often used

---

# Arrays

- `array.length` instead of `len(array)`
- no list comprehensions

---

# Objects

- Keys are always strings
- They do not require quotes

```js
let fruits = {
  apple: 10,
  orange: 5,
  "rotten banana": 1
}
```

---

# Objects

- Members can be addressed using _dot-notation_ or traditional indexes
- Using keys not in the object returns `undefined`

```js
fruits["apple"] // => 10
fruits.apple // => 10
fruits.kiwi // => undefined
```

---

# What's true and false?

False: `null`, `false`, `undefined`, `0`, `""`

Not false:

- `[]` - empty array
- `{}` - empty object

---

# Functions

```js
function add(x, y) {
  return x + y
}
```

---

# Functions

- Use `function` instead of `def`
- Use braces instead of indenting
- Will _never_ give you an error for calling with too few or too many arguments
- No `*args` or `**kwargs` (although destructuring can do the same thing)

```js
function sayHello(name) {
  return `Hello, ${name}!`
}
```

---

# `if` statements

- Predicates require parentheses -- `if (name === 'Marion')`
- Braces instead of indentation
- `else if` instead of `elif`
- Always use `===` instead of `==`!

---

# `for` loops

Looping over an array works _almost_ like you expect:

```js
let letters = ["a", "b", "c"]
for (let letter of letters) {
  console.log(letter)
}
// a
// b
// c
```

---

# Remember to use `of` instead of `in`

`in` loops over the indexes, not the contents of the array.

```js
let letters = ["a", "b", "c"]
for (let letter in letters) {
  console.log(letter)
}
// 0
// 1
// 2
```

---

# `for` loops with numbers

`for` can take three statements: initializing, testing, updating

```js
for (let index = 0; index < 3; index++) {
  console.log(index)
}
// 0
// 1
// 2
```

---

# Using indexes and contents

```js
let nums = [12, 3, 2, 11, 9, -6];

for (let i = 0; i < nums.length; i++) {
  console.log(i, nums[i]);
}
// 0 12
// 1 3
// 2 2
// 3 11
// ...
```

---

# `break` and `continue`

- These work like in Python
- `break` ends the loop
- `continue` starts back at the top of the loop

---

# Other differences you'll see

- `console.log()` instead of `print()`
- Classes and objects
  - `this` instead of `self`
  - `new Book()` instead of `Book()`
  - `constructor()` instead of `__init__()`
- || and && instead of `or` and `and`

---

# Important modern JavaScript features

---

# The spread operator for arrays

The `...` operator allows you to take an array and turn it into separate arguments. This is sometimes used to turn an array into arguments for a function, but can also be used to combine arrays.

```js
let arr1 = [1, 2, 3]
let arr2 = [...arr1, 4, 5, 6]
// => [1, 2, 3, 4, 5, 6]
```

---

# The spread operator for objects

The `...` operator can allow you to combine objects.

```js
let obj1 = {a: 1, b: 2}
let obj2 = {...obj1, c: 3}
// => {a: 1, b: 2, c: 3}
```

---

# Destructuring arrays

```js
let a, b, rest
[a, b, ...rest] = [1, 2, 3, 4, 5]
// a => 1
// b => 2
// rest => 3, 4, 5
```

---

# Destructuring objects

```js
let obj = { a: 1, b: 2, c: 3 }
let { a, b } = obj
// a => 1
// b => 2
```

---

# Classes!

```js
class Person {
  constructor (name) {
    this.name = name
  }

  sayHello () {
    console.log(`Hello ${this.name}!`)
  }
}

const jo = new Person("Jo")
```
