import random

def generate_random_string():
    character_list = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    return ''.join([random.choice(character_list) for _ in range(10)])


print(generate_random_string())