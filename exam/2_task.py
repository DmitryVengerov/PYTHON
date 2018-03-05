# прямой (preorder) - посещаем узел, левое поддерево, правое поддерево;
# обратный (postorder) - посещаем левое поддерево, правое поддерево, узел ;
# симметричный (inorder) - посещаем левое поддерево, узел, правое поддерево;

def preorder(tree, tabs=0):
    ''' Обход в прямом порядке '''
    if tree:
        print('\t'*tabs, get_root_value(tree))
        preorder(get_left_child(tree), tabs + 1)
        preorder(get_right_child(tree), tabs + 1)


def postorder(tree, tabs=0):
    ''' Обход в обратном порядке '''
    # PUT YOUR CODE HERE


def inorder(tree, tabs=0):
    ''' Обход в симметричном порядке '''
    # PUT YOUR CODE HERE

# Обход ранее созданного дерева
'''
>>> preorder(tree)
 a
	 b
	 c
		 d
			 e
>>> postorder(tree)
	 b
			 e
		 d
	 c
 a
>>> inorder(tree)
	 b
 a
	 c
			 e
		 d
'''

