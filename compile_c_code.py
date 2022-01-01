from ctypes import CDLL
from os import system


def compile_c_file(name:str):
    system(f"gcc -shared {name} -o {name}.out")
    return CDLL(f"{name}.out")

def import_c_file(name:str):
    return CDLL(f"{name}.out")





# my_primes = compile_c_file("./main.c")
# print("\n"+ str(my_primes.CfindPrimes(0,10)))