import random
rand_list = [10, 8, 20, 17, 19, 2, 3, 6, 11, 8]

# list_comprehension_below_10 = [x for x in rand_list if x < 10]

list_comprehension_below_10 = list(filter(lambda x: x < 10, rand_list))
