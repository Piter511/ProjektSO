#!/usr/bin/python
import sys
from random import randrange
from operator import itemgetter
import numpy as np
process_que=[]
size=int(input("Podaj ilosc procesow do wygenerowania: "))
zero_arrival=int(input("Czy chcesz aby procesy przyszly w tym samym momencie(TAK=1,NIE=0): "))
def proc_list(x):
    if(x):
        for i in range(size):
            process_que.append([0,randrange(20)+1])#[arrival_time][burst_time] generatng list of random process,
        sorted_arrival_time=sorted(process_que, key=itemgetter(0))#sort by arrival time
    else:
        for i in range(size):
            process_que.append([randrange(20),randrange(20)+1])#[arrival_time][burst_time] generatng list of random process,
        sorted_arrival_time=sorted(process_que, key=itemgetter(0))#sort by arrival time
    return sorted_arrival_time
process_que=proc_list(zero_arrival)
def save_data(process_que):
    f=open(sys.argv[1],"w")
    for i in process_que:
        np.savetxt(f,i)
    f.close()
save_data(process_que)
for i in process_que:
    print(i)


