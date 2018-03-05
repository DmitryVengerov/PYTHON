# Пример бинарного дерева: ((((3+1)×3)/((9−5)+2))−((3×(7−4))+6))
expression = binary_tree('-')
insert_left(expression, '/')
insert_right(expression, '+')
insert_left(get_left_child(expression), '*')
insert_right(get_left_child(expression), '+')
insert_left(get_left_child(get_left_child(expression)), '+')
insert_right(get_left_child(get_left_child(expression)), 3)
insert_left(get_left_child(get_left_child(get_left_child(expression))), 3)
insert_right(get_left_child(get_left_child(get_left_child(expression))), 1)
insert_left(get_right_child(get_left_child(expression)), '-')
insert_right(get_right_child(get_left_child(expression)), 2)
insert_left(get_left_child(get_right_child(get_left_child(expression))), 9)
insert_right(get_left_child(get_right_child(get_left_child(expression))), 5)
insert_left(get_right_child(expression), '*')
insert_right(get_right_child(expression), 6)
insert_left(get_left_child(get_right_child(expression)), 3)
insert_right(get_left_child(get_right_child(expression)), '-')
insert_left(get_right_child(get_left_child(get_right_child(expression))), 7)
insert_right(get_right_child(get_left_child(get_right_child(expression))), 4)

>>> print(expression)
['-', ['/', ['*', ['+', [3, [], []], [1, [], []]], [3, [], []]], ['+', ['-', [9, [], []], [5, [], []]], [2, [], []]]], ['+', ['*', [3, [], []], ['-', [7, [], []], [4, [], []]]], [6, [], []]]]


def print_exp(tree):
    ''' Печать дерева выражений в человеко-читаемой форме '''
    # PUT YOUR CODE HERE

>>> print_exp(expression)
'((((3+1)*3)/((9-5)+2))-((3*(7-4))+6))'