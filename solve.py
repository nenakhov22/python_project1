import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

file1 = open("ratingsdecsription.csv", 'r')
lines = file1.readlines()
lines = [x.replace('\n', '').replace('"', '').split(';') for x in lines]
describe = pd.DataFrame(data=lines[1:], columns=lines[0]).set_index('rtype') #описание критериев

staffmarks = pd.read_csv("staffmarks.csv",sep=';')
students = np.unique(staffmarks['student'].copy()) #множество студентов
staffs = np.unique(staffmarks['staff'].copy())  #множество преподавателей
years = {i: 0 for i in range(2012, 2023)}

for student in students: #считаем количество голосов для каждого года
    temp = staffmarks.loc[staffmarks['student'] == student].copy().set_index('student')
    years_temp = {i: 0 for i in range(2012, 2023)}
    for date in temp['dt']:
        if years_temp[int(date[0:4])] == 0:
            years_temp[int(date[0:4])] = 1
            years[int(date[0:4])] += 1

rates = staffmarks.groupby(['rtype', 'rvalue'])['student'].agg(['count']).copy() #распределения оценок для каждого показателя

teachers_rates_in_total = staffmarks.groupby('staff')['rvalue'].agg(['mean']).copy() #считаем среднюю оценку каждого преподавателя
fig = plt.figure(figsize=(7, 4))
ax = fig.add_subplot()
ax.xaxis.set_major_locator(MultipleLocator(base=1))
ax.bar(list(range(2012, 2023)), [years[i] for i in range(2012, 2023)]) #визуализация первого пункта задачи
ax.set_xlabel('year')
ax.set_ylabel('amount')
fig.suptitle('количество учащихся, проголосовавших за каждый год')
fig1 = [plt.figure(figsize=(7, 4)) for i in range(0, 13)] #для каждого показателя отдельное окно
k = 1
k1 = 0
gs = ''
axis = []
for i in range(0, 13): #визуализация второго пункта задачи
    axis.append(fig1[i].add_subplot())
    axis[i].pie(rates.loc[i+1]['count'], labels=[str(j)+':'+str(rates.loc[i+1].loc[j]['count']) for j in range(1, 6)])
    fig1[i].suptitle(describe.loc[str(i+1)]['name'])

fig2 = plt.figure(figsize=(7, 4)) #первый часть третьего пункта
axx = fig2.add_subplot()
axx.grid()
l = np.linspace(0, 5, 4)
l1 = [0, 0, 0]

file2 = open('output_group1.txt', 'w') #выведем визуализированную информацию в файл 
for index in list(teachers_rates_in_total.index): #распределеим преподавателей по средним оценкам
    if teachers_rates_in_total.loc[index]['mean'] >= l[0] and teachers_rates_in_total.loc[index]['mean'] < l[1]:
        file2.write(index+':низкая оценка\n')
        l1[0] += 1
    elif teachers_rates_in_total.loc[index]['mean'] >= l[1] and teachers_rates_in_total.loc[index]['mean'] < l[2]:
        file2.write(index+':средняя оценка\n')
        l1[1] += 1
    elif teachers_rates_in_total.loc[index]['mean'] >= l[2] and teachers_rates_in_total.loc[index]['mean'] <= l[3]:
        file2.write(index+':высокая оценка\n')
        l1[2] += 1

axx.bar([f'{round(l[i],4)}-{round(l[i+1],4)}' for i in range(3)],l1)

axx.set_ylabel('количество преподавателей')

fig2.suptitle('группы преподавателей по оценкам')


each_p = staffmarks.groupby(['rtype', 'staff'])['rvalue'].agg(['mean']).copy() #считаем средние оценки преподавателей по каждому показателю
#вторая часть третьего пункта
fig3, ax33 = plt.subplots(3, 3)
fig4, ax44 = plt.subplots(2, 2)
k = 1 #счетчик показателей ( от 1 до 13)
fig3.suptitle('группы преподавателей по оценкам по признакам 1-9')
fig4.suptitle('группы преподавателей по оценкам по признакам 10-13')
l1 = [0, 0, 0]
file3 = open("output_group2.txt", 'w') #в файл будем выводить визуализированную информацию
#распределим преподавателей по имеющимся средним оценкам
for i in range(3):
    for j in range(3):
        file3.write('*************   ' + describe.loc[str(k)]['name'] + '  ************  \n')
        for index in list(each_p.loc[k].index):
            if each_p.loc[k].loc[index]['mean'] >= l[0] and each_p.loc[k].loc[index]['mean'] < l[1]:
                file3.write(index + ':низкая оценка\n')
                l1[0] += 1
            elif each_p.loc[k].loc[index]['mean'] >= l[1] and each_p.loc[k].loc[index]['mean'] < l[2]:
                file3.write(index + ':средняя оценка\n')
                l1[1] += 1
            elif each_p.loc[k].loc[index]['mean'] >= l[2] and each_p.loc[k].loc[index]['mean'] <= l[3]:
                file3.write(index + ':высокая оценка\n')
                l1[2] += 1
        ax33[i, j].bar([f'{round(l[i], 4)}-{round(l[i + 1], 4)}' for i in range(3)], l1)
        l1 = [0, 0, 0]
        k += 1
for i in range(2):
    for j in range(2):
        file3.write('*************   ' + describe.loc[str(k)]['name'] + '  ************  \n')
        for index in list(each_p.loc[k].index):
            if each_p.loc[k].loc[index]['mean'] >= l[0] and each_p.loc[k].loc[index]['mean'] < l[1]:
                file3.write(index + ':низкая оценка\n')
                l1[0] += 1
            elif each_p.loc[k].loc[index]['mean'] >= l[1] and each_p.loc[k].loc[index]['mean'] < l[2]:
                file3.write(index + ':средняя оценка\n')
                l1[1] += 1
            elif each_p.loc[k].loc[index]['mean'] >= l[2] and each_p.loc[k].loc[index]['mean'] <= l[3]:
                file3.write(index + ':высокая оценка\n')
                l1[2] += 1
        ax44[i, j].bar([f'{round(l[i], 4)}-{round(l[i + 1], 4)}' for i in range(3)], l1)
        l1 = [0, 0, 0]
        k += 1
file1.close()
file2.close()
file3.close()
plt.show()



