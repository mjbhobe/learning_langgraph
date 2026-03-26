# Learning LangGraph

## Important Non-LangGraph Concepts
It is important that we understand some of Python concepts relevant to LangGraph prohramming before we actually dive into LangGraph. This will help you understand the design & concepts of LangGraph better.

###  Type Annotations
Type annotations are a way to specify the expected type of a variable, function parameter, or function return value. They are _not enforced_ by the Python interpreter, but they can be used by static analysis tools to detect type errors.

### Dictionaries
Granted! Dictionaries are standard Python data structures. However, in the context of LangGraph, we will be using them to store and pass data between nodes in a graph, hence it is important to understand how they work.

Here is a sample dictionary:
```python
ratings = {"movie" : "Avengers End Game", "year" : 2019, "rating" : 8.4}
```
* Dictionaries **allow for efficient data retrieval based on key valued** ```ratings["movie"]``` returns 'Avengers End Game'
* Are **flexible and easy to implement**
* However, it leads to **challenges in ensuring that data is in a particular structure**, especially for larger projects.
* **Doesn't check if data is of the correct type or structure** (for e.g., "rating" : "great" is valid in a dictionary, but it is not a valid rating).This could be a source of errors in your project, and become especially challenging to detect, especially for large codebases.

### Typed Dictionary (```TypeDict```)
Here is an example of how you can create a `TypedDict`.

```python
from typing import TypedDict

class Rating(TypedDict):
    movie : str
    year : int
    rating : float

# this is how to instantiate it
rating = Rating(movie="Avengers End Game", year=2019, rating=8.4)

# you can also pass in a dict with SAME keys wherever the TypedDict is expected
def save_ratings(rating : Rating) -> None:
    ...  # implementation

# this is ok
save_ratings(rating)
# this is ALSO ok
save_ratings({"movie" : "Avengers End Game", "year" : 2019, "rating" : 8.4})
```
**NOTE:** `TypedDict`s are **not enforced** by the Python interpreter, but they can be used by static analysis tools to detect type errors. This helps in **catching errors early** in the development process. They are heavily used in LangGraph to save & pass around graph states.

Another point to note: `TypedDict`s can be _partially initialized_ as follows:

```python
def modify_rating(rating : Rating) -> Rating:
    # just the rating key of the Rating class
    return {"rating" : 9.0}

# this is ok
rating = Rating(movie="Avengers End Game", year=2019, rating=8.4)
rating2 = modify_rating(rating)
print(rating2["rating"])    # will now show 9.0!
```

Here are some _advantages_ of `TypedDict`s:
* **Type Safety**: `TypedDict`s provide type safety by specifying the expected types of the keys and values in a dictionary. This helps in catching type errors early in the development process.
* **Enhanced Readability**: `TypedDict`s make the code more readable by specifying the expected types of the keys and values in a dictionary.
* **Maintainability**: `TypedDict`s make the code more maintainable by specifying the expected types of the keys and values in a dictionary.

### Unions
Here is an example of using a `Union` in Python code:

```python
from typing import Union

def square(x: Union[int, float]) -> float:
    return x * x

print(square(2))      # Ok = 4
print(square(2.5))    # Ok = 6.25
print(square("Hello"))  # Error = can't multiply sequence by non-int of type 'str'
```
Admittedly, the above function is a simple function, which would have failed had I passed in a string even without the Union specifier (because Python does not support string multiplication).

However, consider the following function:

```python
from typing import Union

def add(x: Union[int, float], y: Union[int, float]) -> float:
    return x + y

print(add(1, 2))      # Ok = 3
print(add(1, 2.5))    # Ok = 3.5
print(add("Hello", "World"))  # Error = can't add strings
```

* Unions lets you specify that the type of a parameter could be one of several types. This is especially useful in a non-typed programing language such as Python.
* Flexible and easy to code
* Type safety can provide hints to catch incorrect usage.

The `LangChain` and `LangGraph` (and most other Python libraries) make heavy use of `Unions` and other type hints & annotations for readability and type safety. It is important to understand these concepts before diving into LangGraph.

### Optional
Similar to `Union` is another type annotation called `Optional`. It is a shorthand for `Union[T, None]`. Here is an example of how to use it:

```python
from typing import Optional

def say_hello(name: Optional[str]) -> str:
    if name is None:
        return "Hello World!"
    else:
        return f"Hello {name}, welcome to Python!"

print(say_hello("Manish"))  # will print "Hello Manish, welcome to Python!"
print(say_hello())          # will print "Hello World!"
```

* `Optional[T]` is equivalent to `Union[T, None]`
* It is used to specify that a parameter can be of type `T` or `None` (and **nothing else!**)
* It is a shorthand for `Union[T, None]` (replace `T` with any Python data type)
* It is used to specify that a parameter can be of type `T` or `None` (means can be omitted when function is called)

### Any
`Any` is yet another typed annotation and the easiest to understand. It is used to specify that a parameter can be of **any type**.

```python
from typing import Any

def process(x: Any) -> Any:
    return x

print(process(1))       # Ok = 1
print(process(1.5))     # Ok = 1.5
print(process("Hello")) # Ok = "Hello"
print(process([1, 2, 3])) # Ok = [1, 2, 3]
```

* `Any` is used to specify that a parameter can be of **any type**.
* It is the **least restrictive** type annotation.
* It is **not recommended** to use `Any` in your code, as it defeats the purpose of type annotations.

### Lambda Functions 
Lambda functions are small, anonymous functions in Python. They are defined using the `lambda` keyword and can take any number of arguments, but can only have one expression.

Here is an example of a really simple lambda function:

```python
square =lambda x: x * x
```

This lambda function takes one argument `x` and returns `x * x`. It is equivalent to the following function:

```python
def square(x):
    return x * x
```

Lambda functions are often used in situations where a small function is needed for a short period of time. They are also used in functional programming concepts such as `map`, `filter`, and `reduce`.

Here is an example of using a lambda function with `map`:

```python
map(lambda x: x * x, [1, 2, 3, 4, 5])
```

This will return an iterator that yields the square of each number in the list. It is equivalent to the following:

```python
map(square, [1, 2, 3, 4, 5])
```
Lambda functions are also used in functional programming concepts such as `filter`, `reduce`, and `sorted`.

Here is an example of using a lambda function with `filter`:

```python
filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5])
```

This will return an iterator that yields only the even numbers in the list. It is equivalent to the following:

```python
filter(is_even, [1, 2, 3, 4, 5])
```

Lambda functions are also used in functional programming concepts such as `reduce`, `sorted`, and `map`.

Here is an example of using a lambda function with `reduce`:

```python
reduce(lambda x, y: x + y, [1, 2, 3, 4, 5])
```

This will return the sum of all the numbers in the list. It is equivalent to the following:

```python
reduce(add, [1, 2, 3, 4, 5])
```

Lambda functions are also used in functional programming concepts such as `sorted`, `map`, and `filter`.

Here is an example of using a lambda function with `sorted`:

```python
sorted([1, 2, 3, 4, 5], key=lambda x: x * x)
```

This will sort the list in ascending order based on the square of each number. It is equivalent to the following:

```python
sorted([1, 2, 3, 4, 5], key=square)
```
Lambda functions are a concise way to define small, anonymous functions in Python. They are often used in functional programming concepts such as `map`, `filter`, `reduce`, and `sorted`.

## Elements of LangGraph
Now let us dive into the important elements of LangGraph.

### Graph
* The **Graph** is the main entry point for the application. It is the orchestrator of the application.
* It is a collection of nodes and edges that are connected in a specific order from START to END.
* There could be multiple branches between START and END, and the graph will decide which branch to take based on the state of the application.

### Nodes
* **Nodes** are the fundamental building blocks of a LangGraph application.
* They are the units of computation (i.e. Python functions) that are executed in the graph.
* Each node can be thought of as a function that takes the current state as input and returns the new state as output. A node will typically modify the state of the graph!
* There are two special nodes in the graph - the **START** and the **END** node, which respectively mark the beginning and the end of the graph. You always start the graph from the START node and always end it at END node. These nodes **do not perform any operations**.

### Edges
* **Edges** are the connections between nodes. They define the flow of execution in the graph.
* Edges can be thought of as the paths that the state takes as it moves through the graph.
* Edges can be conditional or unconditional.

#### Conditional Edges
* Conditional edges are _specialized conections_ between nodes, which are not always taken. 
* They are only taken if a certain condition is met, which is usually a result of certain logic applied to the current state of the graph.
* Conditional edges are used to create branches in the graph.

As an example, assume a complex Insuranc claim workflow. Depending on the type of claim, a certain branch of the workflow must be executed - for example car accident claim takes branch A, house fire claim takes branch B and so on. In this case, the conditional edge will check the type of claim and decide which branch to take. 

### State
* The **State** is a shared data structure that holds the context of the application. 
* Simply put, these are elements that are read/changed across as the workflow traverses the nodes of your graph.

As an analogy, think of the state as a whiteboard in a meeting room. Each participant in the meeting(workflow/graph) represents your node in the graph - they can read & write information (state) to the whiteboard. At the end of the meeting, the whiteboard will hold the final state of the meeting.

In LangGraph, the state is a class derived from `TypedDict` that is passed between nodes. Each node can read and modify the state. The state is passed between nodes in the order that they are executed.

### Tools
* **Tools** are Python functions that can be called by the graph to perform certain operations, such as fetching data from a database, performing calculations etc.
* They are used to provide additional functionality to the graph.
* While nodes are part of the graph itself, tools are functionalities used by the nodes themselves.

### ToolNode
* **ToolNode** is a wrapper around a tool that can be used to call the tool from a node.
* It is a convenience class that makes it easier to use tools in a graph.
* Think of a ToolNode as a middle-man between the node and the tool itself - it's main job is to run the tool and connect the tool's output back to the State that is passed around.

#### StateGraph
* A **StateGraph** is a class in LangGraph that is used to build and compile the graph structure.
* It manages the nodes, edges and the overall state, ensuring  that the workflow operates in a unified way and data (state) flows correctly between components.

#### The Car Assembly Line Analalogy

A good analogy that can help you understand all the elements of LangGraph is a car assembly line. 
* The entire factory floor design represents the StateGraph.
* The assembly line represents the Graph. 
* Each station represents a node in the graph.
* The rails connecting the stations represents the edges. 
* The car itself represents the state which is passed between the stations (nodes) of the assembly line (graph).

At each station (node) of the assembly line (graph), certain elements of the car are modified - for example fitting of the engine, fitting of the doors, tires etc. - and the modified car then passes to the next station (node). Think of tools as the specialized equipment used at each station to modify the car - for example the robotic arm that fits the doors, the robotic arm that fits the engine etc. Think of the operator at the station as the ToolNode, who connects the tools to the car (State). The car itself represents the state which is passed across each station (node) in the assembly line (graph). 

The car enters the assembly line at the START station and the finished car exits the assembly line at the END station - no work on the car is done at either the START station or the END station (node).

#### Runnable
All LangChain and LangGraph components implement tha **Runnable** interface - think of them as instances of `Runnable`, which declares the following functions - `invoke()`, `stream()` and `batch()` amongst others. This helps standardize the calling interface between different components of the graph. This is like having a class library of shapes - to abstract a Circle, Rectangle, Square etc. - all of which are derived from the `Shape` class. The `Shape` class can then declare an abstract `draw()` method, which is implemented by each of the derived classes. Now all shapes are _drawable_ - you can call `draw()` on any shape instance and it will work as expected. 

#### Messages
There are 5 main types of messages in LangGraph:
* **HumanMessage** - Represents a message/query from a human user.
* **AIMessage** - Represents a message/response from an AI model.
* **SystemMessage** - Represents a system message that is used to configure the behavior of the AI model.
* **ToolMessage** - Represents a message/response from a tool.
* **FunctionMessage** - Represents a message/response from a function.
 
If you have used the OpenAI API directly, you should already have some idea of these types of messages, especially the first 3.


