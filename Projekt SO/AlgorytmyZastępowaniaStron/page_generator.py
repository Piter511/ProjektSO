#!/usr/bin/python
from random import randrange
import sys
import numpy as np
pages=[] #inicjuje pustą tablice stron
pages_size=int(input("Podaj ilość stron do wygenerowania: "))#długość tablicy, ilość stron
page_range=int(input("Podaj zakres losowania numeracji stron: "))# zekres numeracji od 0 do wartości podanej
def page_list():
    global pages, range
    for i in range(pages_size):
        pages.append([randrange(page_range+1)])
page_list()
def save_data(process_que):#zapisywanie tablicy stron do pliku txt
    f=open(sys.argv[1],"w")
    for i in process_que:
        np.savetxt(f,i)
    f.close()
save_data(pages)
print("Wygenerowane strony: ",end='')
for i in pages:
    print(i[0],end=' ')#wyświetla w terminalu wygenerowany ciąg stron
