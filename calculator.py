"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import re
import traceback
from functools import reduce

def index():
    """ Return a string with instructions on using the app """

    page="""
<h1>Instructions page</h1>
<h3>You can add, subtract, multiply and divide numbers using this app. Here is how:</h3>
<ul>
<li>To add two numbers: add to this page's url '/add/number1/number2'.</li>
<li>To subtract: add to this page's url '/subtract/number1/number2'.</li>
<li>To multiply two numbers: add to this page's url '/multiply/number1/number2'.</li>
<li>To divide a number by another: add to this page's url '/divide/number1/number2'.</li>
</ul>
<p>Example: To get the output for 2+3 ===> '/add/2/3'.<p/>
"""
    return page


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value
    page = """
<h1>{result}</h1>    
""".format(result = sum(args))
    return page

# TODO: Add functions for handling more arithmetic operations.
def multiply(*args):
    """ Return a STRING with the product of the arguments """

    n = 1
    for num in args:
        n *= num
    page = """
<h1>{}</h1>
""".format(n)
    return page


def divide(*args):
    """ Return a string with the quotient of the arguments"""

    try:
        result = reduce((lambda x, y: x//y), args)
    except ZeroDivisionError:
        result = "Cannot divide by zero"
    page = """
<h1>{}</h1>
""".format(result)
    return page


def subtract(*args):
    """ Return a string with the difference between the arguments """

    result = reduce((lambda x, y: x-y), args)
    page = """
<h1>{}</h1>
""".format(result)
    return page


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path. ex.: path = http://localhost:8080/multiply/3/5

    funcs = {
        'add': add,
        'multiply': multiply,
        'divide': divide,
        'subtract': subtract,
        '': index,
    }

    path = path.strip('/').split('/') 
    func_name = path.pop(0)
    args = list(map(int, path))
    try:
        func = funcs[func_name] 
    except KeyError:
        raise NameError
    return func, args
    
    
def application(environ, start_response):
    
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
    