import moment from 'moment'
import React from 'react'
import ReactDOM from 'react-dom'
import PageList from './components/PageList'

const pages = [
  {
    body: "*Python* is an interpreted, high-level, general-purpose programming language. Created by Guido van Rossum and first released in 1991, Python's design philosophy emphasizes code readability with its notable use of significant whitespace. Its language constructs and object-oriented approach aim to help programmers write clear, logical code for small and large-scale projects.\n\nPython is [[dynamically typed|Dynamic programming language]] and garbage-collected. It supports multiple programming paradigms, including procedural, object-oriented, and functional programming. Python is often described as a \"batteries included\" language due to its comprehensive standard library.\n\nPython was conceived in the late 1980s as a successor to the ABC language. Python 2.0, released in 2000, introduced features like list comprehensions and a garbage collection system capable of collecting reference cycles. Python 3.0, released in 2008, was a major revision of the language that is not completely backward-compatible, and much Python 2 code does not run unmodified on Python 3.",
    id: 1,
    title: 'Python',
    updated_at: '2019-12-10 19:52:23.050761',
    updated_by: null
  },
  {
    body: '*Dynamic programming language* in computer science is a class of high-level programming languages, which at runtime, execute many common programming behaviors that static programming languages perform during compilation. These behaviors could include an extension of the program, by adding new code, by extending objects and definitions, or by modifying the type system. Although similar behaviors can be emulated in nearly any language, with varying degrees of difficulty, complexity and performance costs, dynamic languages provide direct tools to make use of them. Many of these features were first implemented as native features in the Lisp programming language. \n\n## Examples\n\nPopular dynamic programming languages include [[JavaScript]], [[Python]], Ruby, PHP, Lua and Perl.',
    id: 2,
    title: 'Dynamic programming language',
    updated_at: '2019-12-10 19:52:23.053777',
    updated_by: null
  },
  {
    body: '*JavaScript*, often abbreviated as JS, is a high-level, just-in-time compiled, object-oriented programming language that conforms to the ECMAScript specification. JavaScript has curly-bracket syntax, [[dynamic typing|Dynamic programming language]], prototype-based object-orientation, and first-class functions.\n\nAlongside HTML and CSS, JavaScript is one of the core technologies of the World Wide Web. JavaScript enables interactive web pages and is an essential part of web applications. The vast majority of websites use it, and major web browsers have a dedicated JavaScript engine to execute it.',
    id: 3,
    title: 'JavaScript',
    updated_at: '2019-12-10 19:52:23.057221',
    updated_by: null
  },
  {
    body: 'I am some test text',
    id: 4,
    title: 'Test page',
    updated_at: '2019-12-10 20:12:31.074511',
    updated_by: 1
  }
]

ReactDOM.render(
  <PageList pages={pages} />,
  document.getElementById('main')
)
