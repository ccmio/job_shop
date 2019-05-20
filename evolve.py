import numpy as np
import random
import js_setting as js
from decode import decode


def cr(population, D):
    t = len(D)
    fitness = []
    for indiv in population:
        fitness.append(indiv[-1])
    Dt = np.var(fitness)
    # print('Dt = ', Dt)
    D.append(Dt)
    Dmax = max(D)
    # print('Dmax = ', Dmax)
    omegle = Dt/Dmax
    # print('omegel = ',omegle)
    CR0 = 1
    beta = 1
    if t == 0:
        CR = CR0  # 交叉概率CR
    else:
        CR = CR0*2**(1-beta*omegle)
    return CR, D


def evolve(population, CR):
    Np = len(population)
    new_population = []
    new_Xh = []
    for h in range(Np):  # 遍历种群中所有个体
        Xh = population[h][0]
        random_list = list(range(0, Np))
        if h in random_list:
            random_list.remove(h)
        h1, h2, h3 = random.sample(random_list, 3)

        Xh1 = population[h1][0]
        Xh2 = population[h2][0]
        Xh3 = population[h3][0]

        r1 = random.randint(0, 2)
        r2 = random.randint(0, 9)
        temp_Xh_i = []

        # Xh进化-------------------------------------------------------------
        for i in range(len(population[h][0])):
            bij = int(js.BS[i] / 50)
            temp_Xh = []
            for j in range(len(population[h][0][i])):
                r3 = random.uniform(0, 1)
                temp_Xh_k = Xh[i][j][:]
                if (i == r1 and j == r2) or (r3 <= CR):
                    maxlist = []
                    minlist = []
                    for k in range(bij):
                        if (Xh2[i][j][k]-Xh3[i][j][k]) != 0:
                            temp_max = max((js.BS[i]-Xh1[i][j][k])/(Xh2[i][j][k]-Xh3[i][j][k]), -Xh1[i][j][k]/(Xh2[i][j][k]-Xh3[i][j][k]))
                            temp_min = min((js.BS[i]-Xh1[i][j][k])/(Xh2[i][j][k]-Xh3[i][j][k]), -Xh1[i][j][k]/(Xh2[i][j][k]-Xh3[i][j][k]))
                        else:
                            temp_max = 100000
                            temp_min = -1
                        maxlist.append(temp_max)
                        minlist.append(temp_min)
                    Fmax = min(2, min(maxlist))
                    Fmin = max(0, max(minlist))
                    F = random.uniform(Fmin, Fmax)
                    Sij = 0
                    m_count = 0
                    for k in range(bij):
                        temp_Xh_k[k] = int(Xh1[i][j][k]+F*(Xh2[i][j][k]-Xh3[i][j][k]))  # 生成Xh'ij
                        if 0 < temp_Xh_k[k] < 50:
                            Sij += temp_Xh_k[k]
                            temp_Xh_k[k] = 0
                        elif temp_Xh_k[k] < 0:
                            temp_Xh_k[k] = 0
                    for value in temp_Xh_k:
                        if value != 0:
                            m_count += 1
                    for k in range(bij):
                        if temp_Xh_k[k] != 0:
                            temp_Xh_k[k] = int(temp_Xh_k[k]+Sij/m_count)
                    temp_list = temp_Xh_k[:]
                    for u in range(len(temp_list) - m_count):
                        temp_list.remove(0)
                    minbn = min(temp_list)
                    temp_Xh_k[temp_Xh_k.index(minbn)] = minbn + js.BS[i] - sum(temp_Xh_k)
                temp_Xh.append(temp_Xh_k)
            temp_Xh_i.append(temp_Xh)
        new_Xh.append(temp_Xh_i)

    # return new_population
    # Yh进化-------------------------------------------------------------------
    Yh_list = []
    new_Yh = []

    for h in range(Np):  # 遍历种群中所有个体
        Yh_list.append(population[h][1])
    half = int(len(Yh_list)/2)
    np.random.shuffle(Yh_list)
    mother = Yh_list[:half]
    father = Yh_list[half:]
    for u in range(half):
        i = random.randint(0, 2)
        j = random.randint(0, 9)
        m_index = []
        f_index = []
        for obj in mother[u]:
            if obj.i == i and obj.j == j:
                m_index.append(mother[u].index(obj))

        for obj in father[u]:
            if obj.i == i and obj.j == j:
                f_index.append(father[u].index(obj))

        son = father[u][:]
        daughter = mother[u][:]
        for i in range(len(m_index)):
            temp = son[f_index[i]]
            son[f_index[i]] = daughter[m_index[i]]
            daughter[m_index[i]] = temp

        new_Yh.append(son)
        new_Yh.append(daughter)

    for h in range(len(new_Yh)):
        new_indiv = []
        for obj in new_Yh[h]:
            obj.size = new_Xh[h][obj.i][obj.j][obj.k]
        schedule, z = decode(new_Yh[h])
        new_indiv.append(new_Xh[h])
        new_indiv.append(new_Yh[h])
        new_indiv.append(z)
        new_population.append(new_indiv)


    return new_population




