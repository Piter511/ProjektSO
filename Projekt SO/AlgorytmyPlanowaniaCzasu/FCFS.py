#!/usr/bin/python
import sys
import numpy as np
import xlwt
from xlwt import Workbook
wb=Workbook()
sheet1 = wb.add_sheet('Sheet 1')
wt=np.empty((0,1),int)
#argumenty przyjmowane przez skrypt muszą być z rozszerzeniem txt
#process[id]=[czas przybycia][czas trwania]
time=0 #licznika czasu
process_que=np.loadtxt(sys.argv[1],int)#przypisujmy do process_que tablice procesów z pliku tekstowego podanego w pierwszym argumencie skryptu
x=int(np.size(process_que)/2)#rozmiar wierszy tablicy
process_que=np.loadtxt(sys.argv[1],int).reshape(x,2)#sprowadzenie tablicy process_que do odpowiedniego formatu z process_que[x] na process_que[x][2]
for i in range(x):
    wt = np.vstack((wt, process_que[i][0]))
f=open(sys.argv[2]+".txt","a")#tworzy plik wynikowy txt podany w drugim argumencie
process_waiting=np.empty((0,2),int)#pusta tablica proccess_waiting dla procesów oczekujących
all_wt=0#suma czasu oczekiwania
all_tat=0#suma czasu całkowitego czasu trwania
sheet1.write(0,1,"Czas przybycia")
sheet1.write(0,2,"Czas trwania")
sheet1.write(0,3,"Czas oczekiwania")
sheet1.write(0,4,"Czas całkowity trwania procesu")
sheet1.write(0,5,"Średni czas czekania procesow")
sheet1.write(0,6,"Średni czas trwania procesow")
for i in range(x):
    sheet1.write(i + 1, 0, "P" + str(i+1))#L.P procesow
    sheet1.write(i + 1, 1, int(process_que[i][0]))#czas przybycia
    sheet1.write(i + 1, 2, int(process_que[i][1]))#czas trwania
    #sheet1.write(i + 1, 3, int(wt[i][0]))#czas oczekiwania
    #sheet1.write(i + 1, 4, int(wt[i][0] + process_que[i][1]))#czas całkowity trwania procesu
print("Przebieg FCFS algorytmu:")
num_task = 1
tat=np.empty((0,1),int)#tabela od całkowitego czasu trwania
for i in range(x):
    tat=np.vstack((tat,process_que[i][1]))
wt=np.empty((0,1),int)#tablica od całkowitego czasu oczekiwania
for i in range(x):
    wt=np.vstack((wt,process_que[i][0]))
service_time=np.empty((0,1),int)
service_time=np.vstack((service_time,wt[0][0]))
while(len(process_que) or len(process_waiting)):#sprawdza dlugosc tablicy process_que i process_waiting
    while (len(process_que) and process_que[0][0] == time):#sprawdza dlugosc tablicy process_que, czy sa jakies procesy i sprawdza czy czas przybycia zgadza sie licznikiem czasu
        if (num_task < x):
            service_time = np.vstack((service_time, service_time[num_task - 1][0] + process_que[0][1]))
            wt[num_task] = service_time[num_task][0] - wt[num_task][0]
            tat[num_task] = wt[num_task] + tat[num_task]
            if (wt[num_task] < 0):
                wt[num_task] = 0
            all_wt += wt[num_task]
            all_tat += tat[num_task]
        num_task += 1#numer wykonywanego zadania
        process_waiting=np.vstack((process_waiting, process_que[0]))#do tablicy proccess_wairing jest dodawany obiekt z tablicy process_waiting
        print("Czas dodania:", time, "Proces dodany", process_waiting[-1])#informuje jaki proces z tablicy został dodany oraz w której jednostce czasu od początku dzialania petli zostal dodany
        f.write("Czas dodania:"+str(time)+" Proces dodany"+str(process_waiting[-1])+"\n")#zapisuje czas dodania oraz informacje o dodanym procesie do do pliku
        process_que=np.delete(process_que, 0, 0)#usuwa proces ostatnio dodany z tablicy process_que
    if (len(process_waiting)):#sprawdza dlugosc tablicy process_waitng, jesli process_waitng jest pusta tablica, to znaczy, że czas przybycia obeiktow jest wiekszy od 0 i licznik dokonac inkkremnetacji
        id_current_process = 0#obecny indeks wykonywanego obiektu z tablicy process_waiting
        print("P",num_task-len(process_waiting),":",process_waiting[id_current_process])# Pi informuje jaki proces jest wykonywany, proces_waiting[id_current_process] informuje o czasie trwania procesu
        f.write("P"+str(num_task-len(process_waiting))+":"+str(process_waiting[id_current_process])+"\n")
        process_waiting[id_current_process][1] -= 1#dekremntuje czas trwania procesu
        if process_waiting[id_current_process][1] == 0:#jesli proces ma jeszcze przydzielony czas nadal bedzie dokonywana dekremntacja czasu trwania
            #print(process_waiting[id_current_process][0])
            process_waiting=np.delete(process_waiting,id_current_process,0)#jeśli czas trwania dobiegnie do konca, proces zostanie usuniety z tablicy process_waiting
    time += 1
for i in range(x):
    sheet1.write(i + 1, 3, int(wt[i][0]))  # czas oczekiwania
    sheet1.write(i + 1, 4, int(tat[i][0]))  # czas całkowity trwania procesu
sheet1.write(1,5,float(all_wt/x))
sheet1.write(1,6,float(all_tat/x))
print("Średni czas czekania procesów: ",float(all_wt/x))
print("Średni czas trwania procesów: ",float(all_tat/x))
f.write("Średni czas czekania procesow:"+str(all_wt/x)+"\n")
f.write("Średni czas trwania procesow:"+str(all_tat/x)+"\n")
sheet1.write(0,7,"Całkowity czas przetwarzania wszystkich procesow")
sheet1.write(1,7,time)
wb.save(sys.argv[2]+".xls")
f.close()