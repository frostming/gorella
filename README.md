# GoRella
[![Build Status](https://travis-ci.org/frostming/gorella.svg?branch=master)](https://travis-ci.org/frostming/gorella)

Monkey patch regular expression methods to built-in string types

## Introduction
This project is aiming at easing the use of regular expression, which is inspired by `RegExp` in JavaScript. The name comes from "gorilla" and "re". The sing-file module will monkey patch the following built-in methods of string types on its import:

- `replace`
- `split` and `rsplit`
- `find` and `rfind`
- `index` and `rindex`
- `partition` and `rpartition`
- `count`
- `startswith` and `endswith`

Besides, it extends the built-in string types with following methods of `re`
module:

- `match`
- `search`
- `findall`
- `finditer`

## Installation
```
$ pip install gorella
``

## Usage
All you need is to import gorella in one line, everything is done for you:
```python
>>> import gorella
>>> 'I am 26 years old.'.search('\d+').group()
'26'
```
For built-in methods, when pass a regular expression object, it will call the corresponding re function, else it falls back to built-in one:
```python
>>> pat = re.compile('\d+')
>>> 'I am 26 years old.'.find('am')
2
>>> 'I am 26 years old.'.find(pat)
5
>>> 'I am 26 years old.'.partition(pat)
('I am ', '26', ' years old')
```
*Because it replaces the pure-C methods with python ones, the performance may be affected.*

## Python 3 support
The monkey patching highly depends on the C-API of CPython, so it doesn't support other implementations than CPython. The test passes on Python 2.6, 2.7, 3.3, 3.4 and 3.5

## License
MIT
