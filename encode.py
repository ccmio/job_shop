import random
import numpy as np
import js_setting as js


# 分批算法，每道工序随机生成子批划分
def create_Xh(BS, S):
    Xh = []
    for i in range(3):
        bij = int(BS[i]/S)  # 最大子批数量
        j_temp_array = []
        for j in range(10):
            cij = random.randint(bij, bij)  # 实际产生子批数量
            if cij != 1:
                k_temp_array = []
                count = 1
                # 随机分配子批量大小
                for k in range(cij-1):
                    temp = random.randint(S, BS[i]-(cij-count)*S-sum(k_temp_array))  # 保证每个子批量大于S小于BSi
                    k_temp_array.append(temp)
                    count += 1
                final_bh = BS[i]-sum(k_temp_array)
                k_temp_array.append(final_bh)
                k_temp_array += [0]*(bij-cij)  # 填充0
                np.random.shuffle(k_temp_array)  # 将工序内划分的子批乱序重排
                j_temp_array.append(k_temp_array)
            # 只分一批的情况分开处理，容易数组越界
            else:
                k_temp_array = [BS[i]] + [0] * (bij - cij)
                np.random.shuffle(k_temp_array)  # 乱序
                j_temp_array.append(k_temp_array)
        Xh.append(j_temp_array)
        # print('工件', i, '-----------------------------------------------------------\n', Xh[i])
    return Xh


# 调度算法
def create_Yh(Xh):
    Yh = []
    for i in range(len(Xh)):
        # J1 J2 J3在构造Xh时已经过乱序排列，确定下了在Yh内的相对位置
        # 这里让J1所有子批作为待插基底，直接分配子批号
        if i == 0:
            for j in range(len(Xh[i])):
                seq = 0
                for batch_size in Xh[i][j]:
                        bn = js.SubBatch(i=i, j=j, k=seq, size=batch_size)
                        Yh.append(bn)
                        seq += 1
        # J2,J3工件的子批以随机插入的方式模拟随机调度
        else:
            pre_p = 0
            # 遍历i的j工序内部子批
            for j in range(len(Xh[i])):
                j_temp = []
                seq = 0
                for batch_size in Xh[i][j]:
                    # 两个常数可控制J2,J3分布范围的控制系数，相加为1，目前为J2 J3倾向分布在中间
                    insert_p = random.randint(pre_p, int(0.5*pre_p)+int(0.5*len(Yh))+1)
                    Yh.insert(insert_p, 0)  # 若把子批任务插入，同一工序内子批前后颠倒，批次很难处理，先插入0标识，再替换
                    bn = js.SubBatch(i=i, j=j, size=batch_size)
                    j_temp.append(bn)
                for temp in range(pre_p, len(Yh)):  # 把0替换为子批
                    if Yh[temp] == 0:
                        j_temp[seq].k = seq
                        Yh[temp] = j_temp[seq]
                        seq += 1
                        pre_p = temp + 1  # 获得下一工序子批分布的起点

    return Yh
