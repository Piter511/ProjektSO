#!/usr/bin/python
import sys
import numpy as np
from xlwt import Workbook
print("Witamy w algorytmie zastępowania stron - FIFO")
wb=Workbook()
sheet1 = wb.add_sheet('Sheet 1')
all_hits=0
all_faults=0
pages=np.loadtxt(sys.argv[1],int)
frame_size=int(sys.argv[2])
pages_size=int(np.size(pages))
def loadLayout(pages):#ładuje układ tabeli w excelu
    sheet1.write(0,0,"Strony")
    for i in range(1,frame_size+1):
        sheet1.write(i,0,"F"+str(i))
    for i in range(np.size(pages)):
        sheet1.write(0,i+1,int(pages[i]))
    sheet1.write(frame_size+2,0,"Wszystkie błędy wymiany strony")
    sheet1.write(frame_size+3,0,"Wszystkie przypadki gdzie nie doszło do błędu wymiany strony")
    sheet1.write(frame_size+4,0,"Współczynnik błędu strony")


loadLayout(pages)
print("Tablica wchodzących stron do symulacji:",pages,"\n")


def FIFO(p,frame):
    global all_hits,all_faults
    pages=[]#tablica pomocnicza
    f=-1
    for i in range(frame):#pętla przyporządkowująca zmienną -1, wartość -1 oznacza ona puste miejsce w ramce
        pages.append(-1)

    for i in range(np.size(p)):
        fault_error=0
        for j in range(frame):#pętla sprawdzająca czy danej kolumnie powtórzyła się strona
            if(pages[j]==p[i]):
                fault_error=1#jeśli tak, to jest ustawiana flaga na trafienie,
                break
        if fault_error==0:
            f=(f+1)%frame#indeks kolumnowy ramek od 0 do frame-1,według którego jest numeraowana talbica pages[]
            pages[f]=p[i]#przypisanie bieżącej strony do pages[f]
            all_faults+=1#zlicza błąd zmiany strony
            print(p[i])
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
            all_hits+=1#zlicza brak wystąpienia błędu strony
            for j in range(frame_size):
                if pages[j]!=-1:
                    print(pages[j])
                    sheet1.write(j + 1, i + 1, int(pages[j]))
                else:
                    print("-")
                    sheet1.write(j + 1, i + 1, "-")#oznaczenie pustej ramki
            print("H")
            sheet1.write(frame+1,i+1,"H")#zapisanie do komórki, że nie doszło do błędu strony
        print()
    sheet1.write(frame_size + 2, 1, all_faults)#zapisuje ilość wszystkich błędy strony do pliku wynikowego
    sheet1.write(frame_size + 3, 1, all_hits)#zapisuje ilość wszystkich miejsc gdzie nie wystąpił błąd
    sheet1.write(frame_size + 4, 1, str(float((all_faults / np.size(p)) * 100)) + "%")#wynik page fault error rate
    print("Wszystkie błędy wymiany strony: ", all_faults)
    print("Wszystkie przypadki gdzie nie doszło do błędu wymiany strony: ", all_hits)

FIFO(pages,frame_size)#wywołuje algorytm FIFO pierwsza zemienna to tablica strony, a druga to rozmiar ramki
wb.save(sys.argv[3]+".xls")