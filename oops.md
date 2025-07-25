# Python OOP Practice: Simplified Learning Summary

This guide simplifies Python's Object-Oriented Programming (OOP) concepts using plain language and structured sections.

---

## 1. Programming Paradigms

* A paradigm is a style or way to structure code.
* OOP is a paradigm focused around **objects**.
* Helps in better modularity, reuse, and managing large codebases.

---

## 2. OOP Basics

### Object-Oriented Programming

* Code is written around **objects**.
* Each object contains data (attributes) and actions (methods).

---

## 3. Four Pillars of OOP

### 1. Encapsulation

* Hide internal details of objects (like private data).
* Example: A bank account class that allows balance checks only via methods.

### 2. Abstraction

* Hide complex parts; show only needed features.
* Example: You use a car via the steering wheel, not its engine internals.

### 3. Inheritance

* Reuse code from parent class into child class.
* Child inherits methods and attributes.

### 4. Polymorphism

* One method behaves differently based on context.
* **Method Overriding**: Child class redefines parent method.
* **Method Overloading**: Same method name, different parameters (Python uses default arguments instead).

---

## 4. Magical / Dunder Methods

| Method                    | Description                                    |
| ------------------------- | ---------------------------------------------- |
| `__init__`                | Constructor; called after object creation.     |
| `__new__`                 | Allocates memory; called before `__init__`.    |
| `__str__`                 | String version for users (e.g., print).        |
| `__repr__`                | Debug-friendly string for developers.          |
| `__call__`                | Makes object callable like a function.         |
| `__eq__`                  | Compares two objects using `==`.               |
| `__add__`                 | Defines behavior of `+` operator.              |
| `__len__`                 | Used when calling `len()` on object.           |
| `__del__`                 | Destructor; cleans up on deletion.             |
| `__getitem__`             | Allows indexing like `obj[key]`.               |
| `__setitem__`             | Allows setting values like `obj[key] = value`. |
| `__contains__`            | Used in `in` keyword checks.                   |
| `__iter__` and `__next__` | Used for iteration and loops.                  |

* `__str__` is for users; `__repr__` is for developers.

---

## 5. OOP Concepts & Decorators

### Method Types

* **Instance Method**: Uses `self`; different for each object.
* **Class Method**: Uses `cls`; shared across all objects. Use `@classmethod`.
* **Static Method**: No `self` or `cls`; behaves like a regular function. Use `@staticmethod`.

### `@property`

* Converts a method into a property (getter).
* Can be combined with a setter.

---

## 6. Module and Package

* **Module**: Any `.py` file.
* **Package**: Folder of modules; used for organized code.

---

## 7. Overriding & Duck Typing

* **Overriding**: Child class customizes inherited methods.
* **Operator Overloading**: Redefine operators like `+`, `==` using magic methods.
* **Duck Typing**: “If it walks like a duck…” — an object is valid if it has needed methods.

---

## 8. Composition vs Aggregation

### Composition

* One class **creates** another inside `__init__`.
* Deleting the outer class also deletes the inner.

### Aggregation

* One class **receives** another as an argument.
* Deleting the source doesn’t delete the reference.

---

## 9. Advanced OOP Concepts

### 1. Metaclass

* A class that defines how other classes behave.
* All classes are created using a metaclass (default is `type`).
* Can be used for auto-registration, validation, etc.

### 2. Singleton Pattern

* Only one instance of a class is ever created.
* Done by overriding `__new__`.

### 3. Factory Pattern

* A method that returns different types of objects based on input.
* Helpful when object creation logic is complex.

### 4. Abstract Base Classes (ABC)

* Define interfaces without implementation using `abc` module.
* Force subclasses to implement required methods.

### 5. Interface vs Implementation

* Interface: What methods/attributes a class should have.
* Implementation: How those methods actually work.

---

## 10. Iterable Protocol

### Iterable

* Has `__iter__()` method.
* Returns an iterator.

### Iterator

* Has both `__iter__()` and `__next__()`.

* Used to loop over objects.

* Lists are iterable, but not iterators.

* `iter(list)` returns a list-iterator.

---

## 11. Python Unified Type System

* Everything is an object (int, str, list, functions, etc.).
* All objects have:

  * Type (its class)
  * Identity (unique memory location)
  * Value (data)

### Type Hierarchy

```
object <- int
       <- str
       <- list
       <- function
       <- YourClass
```

* All classes inherit from `object`.
* All classes are instances of the metaclass `type`.

---

*End of OOP Summary*
