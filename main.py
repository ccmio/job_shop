from encode import create_Xh
from encode import create_Yh
from decode import decode
from evolve import cr
from evolve import evolve
from selection import select
from selection import search
import js_setting as js

# 初始化种群，个体数50
def create_populaion():
    population = []
    for i in range(10):
        Xh = create_Xh(js.BS, 50)
        Yh = create_Yh(Xh)
        schedule, z = decode(Yh)
        indiv = [Xh, Yh, z]
        population.append(indiv)
    return population, Xh, Yh, schedule, z


population, Xh, Yh, schedule, z = create_populaion()
D = []

# 进化1000次
for i in range(100):
    fitness = []
    CR, D = cr(population, D)
    new_population = evolve(population, CR)
    child_population = select(population, new_population)
    final_population = search(child_population)
    population = final_population
    for invid in final_population:
        fitness.append(invid[-1])
    print('训练第', i, '次', '适应度：', max(fitness))
    print('-------------------------------------------------------------')

fitness = []
for invid in population:
    fitness.append(invid[-1])
index = fitness.index(max(fitness))
print('最快完成时间：', int(1000000/max(fitness)), 's')
print('划分方案:')
print(population[index][0])
schedule, z = decode(population[index][1])
print('调度方案:')
for i in range(len(schedule)):
    for j in range(len(schedule[i])):
        print('machine',i,'-',j,)
        for obj in schedule[i][j]:
            if js.WT[obj.i][obj.j] != 0:
                print('i=',obj.i,'j=',obj.j,'k=',obj.k)

