# 数据及类对象设置文件

# work time of each type of machine
# WT[job][process]
WT = [[275, 120, 142, 0, 215, 316, 291, 514, 0, 101],
      [170, 240, 84, 96, 0, 0, 158, 0, 344, 94],
      [364, 0, 78, 199, 474, 0, 122, 612, 122, 210]]

# prepare time
# PT[from][to][process]
PT = [[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 1, 1, 0, 0, 0, 2, 0, 0, 2],
       [1, 0, 1, 0, 2, 0, 1, 2, 0, 2]],
      [[2, 1, 1, 0, 0, 0, 1, 0, 0, 2],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [2, 0, 4, 3, 0, 0, 1, 0, 2, 1]],
      [[2, 0, 1, 0, 1, 0, 2, 3, 0, 1],
       [2, 0, 3, 4, 0, 0, 3, 0, 1, 2],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]]

# load time
# LT[job][early/late]
LT = [[0, 0],
      [0, 50000],
      [100000, 150000]]

# batch size
# BS[job]
BS = [300, 150, 200]

# amount of machine
# AM[process]
AM = [1, 2, 3, 3, 3, 2, 2, 4, 1, 1]


# 子批任务类
class SubBatch:
    def __init__(self, i, j, size, k=-1, start=0, end=0):
        self.i = i  # 工件类别
        self.j = j  # 工序号，由于包括了0加工工序，所以实际上对应加工机器的类别号
        self.k = k  # 子批次
        self.size = size  # 子批批量
        self.start = start
        self.end = end