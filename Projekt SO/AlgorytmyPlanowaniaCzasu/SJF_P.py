#!/usr/bin/python
import sys
import numpy as np
from operator import itemgetter
import xlwt
from xlwt import Workbook
wb=Workbook()
sheet1 = wb.add_sheet('Sheet 1')
all_wt = 0#suma wszystkich całkowitych czasów czekania
all_tat = 0#suma wszystkich całkowitych czasów trwania
time=0 #clock_count
process_que=np.loadtxt(sys.argv[1],int)
x=int(np.size(process_que)/2)
process_que=np.loadtxt(sys.argv[1],int).reshape(x,2)#proces[czas przybycia][czas trwania]
p_id=np.array(range(x)).reshape(x,1)#_id[0,x-1]
process_que=np.append(process_que,p_id,axis=1)#proces[czas przybycia][czas trwania][p_id], dodajemy id_p aby zachować rozróżnalność procesów
f=open(sys.argv[2]+".txt","w")#tworzy plik wynikowy z przebiegiem eksperymentu .txt
wt=np.empty((0,1),int)
for i in range(x):
    wt=np.vstack((wt,process_que[i][0]))

def loadLayout():
    sheet1.write(0, 1, "Czas przybycia")
    sheet1.write(0, 2, "Czas trwania")
    sheet1.write(0, 3, "Czas oczekiwania")
    sheet1.write(0, 4, "Czas całkowity trwania procesu")
    sheet1.write(0, 5, "Średni czas czekania procesow")
    sheet1.write(0, 6, "Średni czas trwania procesow")
    sheet1.write(0, 7, "Całkowity czas przetwarzania wszystkich procesow")
    for i in range(x):
        sheet1.write(i + 1, 0, "P" + str(i + 1))  # L.P procesow
        sheet1.write(i + 1, 1, int(process_que[i][0]))  # czas przybycia
        sheet1.write(i + 1, 2, int(process_que[i][1]))  # czas trwania

loadLayout()
process_waiting=np.empty((0,3),int)#queue for waiting proecess
print("Przebieg algorytmu SJF wywłaszczeniowego:")
num_task=1
group=1
entry_process=np.empty((0,3),int)#historia wprowadzonych procesów do kolejki, zapisuje po kolej dodane obiekty do symulacji
token=True#token stwierdzający czy wszystkie procesy przychodzą w róznym czasie
while(len(process_que) or len(process_waiting)):
    while (len(process_que) and process_que[0][0] == time):
        process_waiting=np.vstack((process_waiting, process_que[0]))
        entry_process = np.vstack((entry_process, process_que[0]))
        f.write("Czas dodania:"+str(time)+" Proces dodany P"+str(process_waiting[-1][2]+1)+": "+"[ "+str(process_waiting[-1][0])+","+str(process_waiting[-1][1])+" ]"+"\n")#zapis do pliku txt
        print("Czas dodania:", time, "Proces dodany", "[",process_waiting[-1][0],",",process_waiting[-1][1],"]")
        process_que=np.delete(process_que, 0, 0)#usuwanie procesu,który już zdążył przybyć
        process_waiting = sorted(process_waiting, key=itemgetter(1))#sortowanie listy czasów trwania procesów które JUŻ nadeszły od najmniejesz do największej


    if (len(process_waiting)):  #sprawdza czy jest już jakiś oczekujący proces, jeśli brak, inkrementuje zmienną time
        time_1=time+1#time_1 to zmienna pomocnicza, pętla wewn. modyfikuje time przez co w pliku .txt czas dodania dla wszystki P# wynosi 0 dla procesów o różnym czasie przyjścia
        id_current_process = 0
        print("P"+str(process_waiting[id_current_process][2]+1)+":","[",process_waiting[id_current_process][0],",",process_waiting[id_current_process][1],"]")
        f.write("P"+str(process_waiting[id_current_process][2]+1)+":"+"[ "+str(process_waiting[id_current_process][0])+","+str(process_waiting[id_current_process][1])+" ]"+"\n")
        process_waiting[id_current_process][1] -= 1
        if process_waiting[id_current_process][1] == 0:#warunek sprawdzający czy dany proces się zakończył
            wt[id_current_process] = time - process_waiting[id_current_process][0] - entry_process[process_waiting[id_current_process][2]][1]+1
            sheet1.write(process_waiting[id_current_process][2] + 1, 3,
                         int(wt[id_current_process][0]))  # zapis do xls całkowitego czasu oczekiwania dla konkretnego procesu
            sheet1.write(process_waiting[id_current_process][2] + 1, 4,
                         int(wt[id_current_process][0] + entry_process[process_waiting[id_current_process][2]][1]))  # zapis do xls całkowitego czasu trwania dla konkretnego procesu
            all_wt = all_wt + wt[id_current_process][0]#liczenie całkowitego czasu czekania wszystkich procesów
            all_tat = all_tat + wt[id_current_process][0] + entry_process[process_waiting[id_current_process][2]][1]#liczenie całkowitego czasu trwania wszystkich procesów
            process_waiting=np.delete(process_waiting,id_current_process,0)#usuwanie wykonanego zadania z listy process_waiting
    time += 1

print("Czas trwania algorytmu: ",time)
print("Średni czas czekania: ",all_wt/x)
print("Średni czas trwania: ",all_tat/x)
f.write("Średni czas czekania: "+str(all_wt/x))
f.write("Średni czas trwania: "+str(all_tat/x))
sheet1.write(1, 5, all_wt / x)
sheet1.write(1, 6, all_tat / x)
sheet1.write(1,7,time)
wb.save(sys.argv[2]+".xls")