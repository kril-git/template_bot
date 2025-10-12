'''
Замыкание. 
'''

from functools import wraps
from time import sleep
from typing import Any


def multiply(num1):
    var = 10
    def inner(num2):
        return num1 + " " + num2 + " " + str(var)
    return inner


one = multiply("one")
two = multiply("two")

# print(one.var)

print(one("One num2"))
print(two("Two_num2"))

print(one.__closure__)


def func1():
    a = 1
    b = "line"
    c = [1, 2, 3]
    d = "line2"
    
    def func_out():
        nonlocal a
        a +=  2
        c.append(4)
        return a, b, c, d

    return func_out


print("****************************************************")
fn = func1()
fn()
print(fn.__closure__)
for i in fn.__closure__:
    print(i, i.cell_contents)


# def verbose(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         print(func.__name__)
#         return func(*args, **kwargs)
#     return wrapper

def verbose(func):
    @wraps(func)
    def wrapper(str):
        print(func.__name__)
        return func(str)
    return wrapper


@verbose
def upper(str):
    return str.upper()
        

print("*****************************************************")

print(upper("line"))



print("*****************************************************")
print("*****************************************************")

def parent():
    print('=> parent')
    def child():
        print('=> I child function')
        def child2():
            print("=> I am child @")
            return child2
    return child


p = parent()
p2 = p()


class Delayed:
    
    def __init__(self, delay = 1):
        self._delay = delay
        
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f'Спим {self._delay} сек.')
            sleep(self._delay)
            val = func(*args, **kwargs)
            return val
        return wrapper
    
@Delayed(delay=0.5)
def countdown(int_num):
    if int_num < 1:
        # exit(0)
        return 0
    else:
        print(int_num)
    countdown(int_num - 1)
   
countdown(3)
print("+++++++++++++++++++++++++++++++++++++++++++")
@Delayed(delay=1)
def countdown2(int_num):
    print(int_num)


print("+++++++++++++++++++++++++++++++++++++++++++")

for i in range(3):
    countdown2(i)


# def outer():
#     n = 5
#     def inner():
#         nonlocal n
#         n += 1
#         print(n)
#     return inner

# fn = outer()

# fn()
# fn()


# def multiply(n):
#     def inner(m):
#         return n*m
#     return inner

# fn1 = multiply(5)

# print(fn1(6))
# print(fn1(7))


# '''
# Декораторы в Python представляют функцию, которая в качестве параметра получает функцию и в качестве результата
# также возвращает функцию. Декораторы позволяют модифицировать выполняемую функцию, 
# значения ее параметров и ее результат без изменения исходного кода этой функции.
# '''

# # определение функции декоратора
# def select(input_func):    
#     def output_func():      # определяем функцию, которая будет выполняться вместо оригинальной
#         print("*****************")  # перед выводом оригинальной функции выводим всякую звездочки
#         input_func()                # вызов оригинальной функции
#         print("*****************")  # после вывода оригинальной функции выводим всякую звездочки
#     return output_func     # возвращаем новую функцию
 
 
#  # определение функции декоратора
# def select1(input_func):    
#     def output_func():      # определяем функцию, которая будет выполняться вместо оригинальной
#         print("*****************")  # перед выводом оригинальной функции выводим всякую звездочки
#         res = input_func()                # вызов оригинальной функции
#         print("*****************")  # после вывода оригинальной функции выводим всякую звездочки
#         return res
#     return output_func     # возвращаем новую функцию

#  # определение функции декоратора
# def select2(input_func):    
#     def output_func(*args):      # определяем функцию, которая будет выполняться вместо оригинальной
#         print("*****************")  # перед выводом оригинальной функции выводим всякую звездочки
#         res = input_func(*args)                # вызов оригинальной функции
#         print("*****************")  # после вывода оригинальной функции выводим всякую звездочки
#         return res
#     return output_func     # возвращаем новую функцию

# # определение оригинальной функции
# @select         # применение декоратора select
# def hello():
#     print("Hello METANIT.COM")
    
# @select1
# def fn_temp():
#     x = 5
#     y = 50
#     return x * y
 
 
# @select2
# def summ(a, b):
#      return a + b
 
# # вызов оригинальной функции
# hello()

# print(fn_temp())

# print(summ(5, 7))


# /Users/kril/python_prj/deploy_bot/requirements.txt