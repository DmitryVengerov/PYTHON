# bones game

import random

def greatings():
    print('Welcome to the best game in the world')
    menu()

def menu():
    print('Did you wanna play in my game? [y/n]')
    userInput = input()
    if userInput == 'y':
        dialog()
    else:
        credits()

def dialog():
    print('OK! How much you bet?')
    acc = int(input())
    print('OK!')
    start(acc)

def start(acc_user):
    array = [2,3,4,5,6,7,8,9,10,11,12]
    acc = acc_user
    if acc in array:
        print("User put on "+ str(acc))
        drop_comp = drop_bones()
        print("Bones drop -> "+ str(drop_comp))
        win_stat = comparison(acc, drop_comp)
        next_step(win_stat, drop_comp)
    else:
        print('You have error')

def credits():
    print("Bye-bye sweet pie")
    print("Createt by        hardbeat34")

def comparison(acc, drop):
    if acc <= drop:
        # sec
        return 1
    else:
        # fail
        return 0

def next_step(result, drop_comp):
    score = 0
    if result == 1:
        score =+ drop_comp
        print("Your score " + str(drop_comp))
        check_score(result ,score)
        menu()
    else:
        score =- drop_comp
        print("Your score " + str(drop_comp))
        check_score(result, score)
        menu()

def check_score(result, score):
    if score != result :
        print("failed")
    else:
        print("win")

# имитируем просок костей
def drop_bones():
    return random.randint(1,6) + random.randint(1,6)


if __name__ == '__main__':
    greatings()
