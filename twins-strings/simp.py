def f(lst):
     i = 0
     upper = len(lst) - 1
     while i < upper:
         a, b = lst[i], lst[i + 1]
         if a % 2 == 0 and b % 2 != 0 \
         or a % 2 != 0 and b % 2 == 0:
             lst[i], lst[i + 1] = b, a
             i += 1
         i += 1
     return lst
 f([1, 1, 2, 1, 1])