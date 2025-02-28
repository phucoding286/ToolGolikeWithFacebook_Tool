import time
import random
from modules import system_color, success_color

def rdn_wait(t=10, f=1):
    while True:
        do = [True for _ in range(t)] + [False for _ in range(f)]
        if random.choice(do):
            print(success_color("[#] Máy đã chọn hành động."))
            return 0
        else:
            print(system_color("[!] Máy chưa chọn tiếp tục hành động 2s ..."))
            time.sleep(2)

def rdn_do(t=10, f=1):
    do = [True for _ in range(t)] + [False for _ in range(f)]
    return random.choice(do)