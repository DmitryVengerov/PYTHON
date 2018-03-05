def binary_tree(value):
    ''' Создание бинарного дерева, со значением value в корне '''
    return [value, [], []]

def insert_left(root, value):
    ''' Создание нового поддерева, как левого потомка для узла root '''
    # PUT YOUR CODE HERE
    temp = binary_tree(value)
    root[1] = temp
    return root

def insert_right(root, value):
    ''' Создание нового поддерева, как правого потомка для узла root '''
    temp = binary_tree(value)
    root[2] = temp
    return root

def get_root_value(root):
    ''' Получить значение в корне (указанном узле)  root '''
    return root[0]

def set_root_value(root, new_value):
    ''' Установить новое значение new_value в корне (указанном узле) root '''
    root[0] = new_value

def get_left_child(root):
    ''' Получить левого потомка для узла root '''
    return root[1]

def get_right_child(root):
    ''' Получить правого потомка для узла root '''
    return root[2]

def preorder(tree, tabs=0):
    ''' Обход в прямом порядке '''
    if tree:
        print('\t'*tabs, get_root_value(tree))
        preorder(get_left_child(tree), tabs + 1)
        preorder(get_right_child(tree), tabs + 1)

def postorder(tree, tabs=0):
    ''' Обход в обратном порядке '''
    if tree:
        postorder(get_left_child(tree), tabs + 1) 
        postorder(get_right_child(tree), tabs + 1) 
        print('\t'*tabs, get_root_value(tree))    

def inorder(tree, tabs=0):
    ''' Обход в симметричном порядке '''
    if tree:
        inorder(get_left_child(tree), tabs + 1) 
        print('\t'*tabs, get_root_value(tree)) 
        inorder(get_right_child(tree), tabs + 1)

def print_exp(tree):
    # python 3.6 - in string usr end=''
    temp = []
    if tree:
        # if we use root value we make expression like ((3)+(1))
        # in other way we found all childrens
        if(get_left_child(tree)):
            print('(',end='')
            print_exp(get_left_child(tree))
            print(get_root_value(tree),end='')
            print_exp(get_right_child(tree))
            print(')',end='')
        else:
            print_exp(get_left_child(tree))
            print(get_root_value(tree),end='')
            print_exp(get_right_child(tree))

def build_exp_tree(exp_string):
    '''
    Построить дерево выражений по строке exp_string
    Ваш код должен быть здесь
    '''
    if exp_string:
        exp_string = exp_string.replace(' ','')
                

    return exp_string
    

if __name__ == '__main__':
    # 1 
    tree = binary_tree('a')
    insert_left(tree, 'b')
    insert_right(tree, 'c')
    insert_right(get_right_child(tree), 'd')
    insert_left(get_right_child(get_right_child(tree)), 'e')
    # 2
    #preorder(tree)
    #postorder(tree)
    #inorder(tree)
    # 3
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
    #print_exp(expression)
    # 4
    #exp_tree = build_exp_tree('((8 + 7)/(10 - 4))')
    exp_tree = build_exp_tree('((8 + 7)/(10 - 4))')
    #print(exp_tree)
'''
def build_exp_tree(exp_string):
    Построить дерево выражений по строке exp_string
     Ваш код должен быть здесь
    pass

    >>> exp_tree = build_exp_tree('((8 + 7)/(10 - 4))')
    >>> print_exp(exp_tree)
    '((8 + 7)/(10 - 4))'
'''

