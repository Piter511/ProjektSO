#!/usr/bin/python
import sys
import numpy as np
from xlwt import Workbook
print("Witamy w algorytmie zastępowania stron - LRU")
wb=Workbook()
sheet1 = wb.add_sheet('Sheet 1')
all_hits=0
all_faults=0
pages=np.loadtxt(sys.argv[1],int)
frame=int(sys.argv[2])
pages_size=int(np.size(pages))
def loadLayout(pages):#ładuje układ tabeli w excelu
    sheet1.write(0,0,"Strony")
    for i in range(1, frame + 1):
        sheet1.write(i,0,"F"+str(i))
    for i in range(np.size(pages)):
        sheet1.write(0,i+1,int(pages[i]))
    sheet1.write(frame + 2, 0, "Wszystkie błędy wymiany strony")
    sheet1.write(frame + 3, 0, "Wszystkie przypadki gdzie nie doszło do błędu wymiany strony")
    sheet1.write(frame + 4, 0, "Współczynnik błędu strony")


loadLayout(pages)
print("Tablica wchodzących stron do symulacji:",pages,"\n")


def LRU(p,frame):
    global all_hits,all_faults
    pages=[]#tablica pomocnicza
    history_stack = []#stos zapamiętujący wchodzące procesy, strona najdłużej nie używana znajduje się na spodzie stosu

    f=0
    for i in range(frame):#pętla przyporządkowująca zmienną -1, wartość -1 oznacza ona puste miejsce w ramce
        pages.append(-1)

    for i in range(np.size(p)):
        fault_error=0
        for j in range(frame):#pętla sprawdzająca czy danej kolumnie powtórzyła się strona
            if(pages[j]==p[i]):
                fault_error=1#jeśli tak, to jest ustawiana flaga na trafienie,
                break

        if fault_error==0:
            all_faults+=1#zlicza błąd zmiany strony
            history_stack.insert(-i-1,p[i])#dodanie wchodzącej strony do stosu
            print(p[i])
            if pages[f]!=-1:
                l_recent = 99999999
                for j in range(frame):#pętla szukająca
                    lru_flag=0#flaga na nową stronę,
                    currentHistorylen=len(history_stack)#ilość stron, które już wszedły do symulacji, żeby wyszukiwanie strony dawno używanej odbyło się po długości bieżacej tablicy
                    while currentHistorylen >= 0:#pętla obliczająca czy "odległości" w tablicy dla poszczególnych elementów w tablicy pages
                        currentHistorylen-=1
                        #wyszukiwanie odbywa się od początku tablicy history_stack
                        #element na początku tablicy to ostatnie odwołania
                        if pages[j]==history_stack[-currentHistorylen]: #sprawdzenie od początku tablicy elementu w obecnej kolumnie(pages) w history_stack
                            lru_flag=1#odnalezienie elementu obecnej strony w kolumnie w history stack, zatrzymanie dekrementacji currentHistorylen
                            break
                    if(lru_flag==1 and l_recent > currentHistorylen):#gdy odnajdzie najstarszy element w historii, aktualizuje najdłużej nieużywaną stronę element
                                                                     #im j większe to strona staje się najdawniej używana i podlega wymianie nową stroną
                        l_recent=currentHistorylen#zmienna przechowująca
                        f=j #indeks w supp pages dla najstarszego elementu

            pages[f]=history_stack[-i-1]#przypisanie do elementu najrzadziej używanego w tablicy pages, strony ostatnio dodanej do history_stack
            f=(f+1)%frame
            for j in range(frame):
                if pages[j]!=-1:
                    print(pages[j])
                    sheet1.write(j+1,i+1,int(pages[j]))
                else:
                    print("-")
                    sheet1.write(j+1,i+1,"-")
            print("F")
            sheet1.write(frame+1,i+1,"F")#zapisanie do komórki czy w danej stronie doszło do błędu strony
        else:#zapisuje poprzednią kolumnę ze stronami, jeśli nie wystąpił bład strony
            history_stack.insert(-i - 1, p[i])#jeśli strona jest załadowana, numer strony w stosie wędruje na samą górę
            #for y in range(i-1):
                #if history_stack[y]==history_stack[-1]:
                    #history_stack.pop(history_stack[y])
            all_hits+=1#zlicza brak wystąpienia błędu strony
            for j in range(frame):
                if pages[j]!=-1:
                    print(pages[j])
                    sheet1.write(j + 1, i + 1, int(pages[j]))
                else:
                    print("-")
                    sheet1.write(j + 1, i + 1, "-")#oznaczenie pustej ramki
            print("H")
            sheet1.write(frame+1,i+1,"H")#zapisanie do komórki, że nie doszło do błędu strony
        print()
    sheet1.write(frame + 2, 1, all_faults)#zapisuje ilość wszystkich błędy strony do pliku wynikowego
    sheet1.write(frame + 3, 1, all_hits)#zapisuje ilość wszystkich miejsc gdzie nie wystąpił błąd
    sheet1.write(frame + 4, 1, str(float((all_faults / np.size(p)) * 100)) + "%")#wynik page fault error rate
    print("Wszystkie błędy wymiany strony: ", all_faults)
    print("Wszystkie przypadki gdzie nie doszło do błędu wymiany strony: ", all_hits)


LRU(pages, frame)#wywołuje algorytm LRU pierwsza zemienna to tablica strony, a druga to rozmiar ramki
wb.save(sys.argv[3]+".xls")