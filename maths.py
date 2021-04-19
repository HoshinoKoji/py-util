import random

def gen_mul_problem_within_100(remove_easy_problems=True, str_output=True):
    problem = random.randint(10, 99), random.randint(10, 99)
    if remove_easy_problems:
        while (problem[0] % 10 == 0) or (problem[1] % 10 == 0):
            problem = random.randint(10, 99), random.randint(10, 99)
    return f'{problem[0]} × {problem[1]} = ' if str_output else problem