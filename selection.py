import random
import math
import js_setting as js
from decode import decode


def select(population, new_population):
    total_population = population + new_population
    fitness = []
    fitness_sum = []
    child_population = []

    for indiv in total_population:
        fitness.append(math.exp(indiv[-1]))

    # 精英保留策略，最优个体直接进下一轮
    max_index = fitness.index(max(fitness))
    child_population.append(total_population[max_index])
    min_index = fitness.index(min(fitness))
    total_population.remove(total_population[min_index])

    fitness.pop(min_index)
    sumx = sum(fitness)

    # 轮盘赌选择
    for i in range(len(total_population)):
        if i == 0:
            fitness_sum.append(fitness[i] / sumx)
        else:
            fitness_sum.append(fitness[i] / sumx + fitness_sum[i - 1])

    for i in range(len(total_population)):
        rand = random.uniform(0, 1)
        for j in range(len(total_population)):
            if j == 0:
                if 0 < rand <= fitness_sum[j]:
                    child_population.append(total_population[j])
            else:
                if fitness_sum[j - 1] < rand <= fitness_sum[j]:
                    child_population.append(total_population[j])

    # 精英保留策略，删除筛选后的最弱个体
    child_population.sort(key=(lambda x:x[-1]))
    length = len(child_population)
    # 如果取最优的一半样本，非常容易进入局部最优出不来，这里取了第2/4，第4/4部分，效果好一些
    child_population = child_population[int(length/4):int(length/2)] + child_population[int(length*3/4):]

    # 返回本代幸存个体
    return child_population


def search(child_population):
    final_population = child_population
    for i in range(len(final_population)):
        x = final_population[i][0][:]
        y = final_population[i][1][:]
        d = random.randint(1, 128)
        i = y[d].i
        j = y[d].j
        k = y[d].k
        d_search = d
        r = random.randint(0, 1)
        if r == 0:
            if j > 1:
                for obj in y:
                    if obj.i == i and obj.j == j-1 and obj.k == js.BS[i]/50-1:
                        d1 = y.index(obj)
                        continue
            else:
                d1 = 0
                d_search = d - 1
            while d_search > d1+1:  # 前向搜索
                if (y[d_search].i == i and y[d_search].j == j) and (y[d_search].k > 0):
                    temp = x[i][j][k]
                    x[i][j][k] = x[i][j][k-1]
                    x[i][j][k-1] = temp
                    k -= 1
                    temp = y[d].size
                    y[d].size = y[d_search].size
                    y[d_search].size = temp
                    _, fxy = decode(y)
                    fxhyh = final_population[i][-1]
                    if fxy > fxhyh:
                        final_population[i][0] = x
                        final_population[i][1] = y
                        final_population[i][-1] = fxy
                    d = d_search
                d_search -= 1

        else:   # 后向搜索
            if j < 9:
                for obj in y:
                    if obj.i == i and obj.j == j + 1 and obj.k == 0:
                        d2 = y.index(obj)
                        continue
            else:
                d2 = len(y)+1
                d_search = d + 1
            while d_search < d2-1:
                if (y[d_search].i == i and y[d_search].j == j)and (y[d_search].k < js.BS[i]/50-1):
                    temp = x[i][j][k]
                    x[i][j][k] = x[i][j][k + 1]
                    x[i][j][k + 1] = temp
                    k += 1
                    # 原来同时操作交换子批类对象和对象的批次信息，总会出现交换失效的情况，出的错依然没找出来
                    # 但由于Yh中存有批量信息，所谓的交换位置，其实直接交换批量信息就可以，错误排除
                    temp = y[d].size
                    y[d].size = y[d_search].size
                    y[d_search].size = temp
                    d = d_search
                    _, fxy = decode(y)
                    fxhyh = final_population[i][-1]
                    if fxy > fxhyh:
                        final_population[i][0] = x
                        final_population[i][1] = y
                        final_population[i][-1] = fxy
                d_search += 1

    return final_population
