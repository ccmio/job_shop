def debug(yh):
    checklist = [[[],[],[],[],[],[],[],[],[],[]],
                 [[],[],[],[],[],[],[],[],[],[]],
                 [[],[],[],[],[],[],[],[],[],[]]]
    for obj in yh:
        checklist[obj.i][obj.j].append(obj.k)
    flag = 0
    for i in range(len(checklist)):
        for j in range(len(checklist[i])):
            if sorted(checklist[i][j]) != checklist[i][j]:
                print('{}号工件{}号工序排序错误'.format(i,j))
                flag = 1
                print(checklist[i][j],'\n')

    if flag == 0:
        print('无错误')
    return
