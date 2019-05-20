import random
import js_setting as js
import numpy as np


def decode(yh):
    Yh = yh

    arrive_j1 = random.randint(0, 50000)
    arrive_j2 = random.randint(100000, 150000)
    R = [0, arrive_j1, arrive_j2]
    end_time = [[],
                [],
                []]
    schedule = [[[]],
                [[], []],
                [[], [], []],
                [[], [], []],
                [[], [], []],
                [[], []],
                [[], []],
                [[], [], [], []],
                [[]],
                [[]]]
    count = 0
    for obj in Yh:
        temp_start = []
        temp_end = []
        work = js.WT[obj.i][obj.j] * obj.size
        for seq_machine in schedule[obj.j]:
            if not seq_machine:
                prepare = 0
                if js.WT[obj.i][obj.j] == 0:
                    start, end = end_time[obj.i][obj.j - 1], end_time[obj.i][obj.j - 1]
                elif obj.j == 0 and obj.k == 0:
                    start = R[obj.i]
                elif obj.j > 0:
                    start = end_time[obj.i][obj.j-1]
                end = start + prepare + work
                temp_start.append(start)
                temp_end.append(end)
            else:
                last_job = seq_machine[-1]
                prepare = js.PT[last_job.i][obj.i][obj.j]
                if js.WT[obj.i][obj.j] == 0:
                    start, end = end_time[obj.i][obj.j-1], end_time[obj.i][obj.j-1]
                elif obj.j == 0 and obj.k == 0:
                    start = max(last_job.end, R[obj.i])
                elif obj.j == 0 and obj.k > 0:
                    start = last_job.end
                elif obj.j > 0:
                    start = max(last_job.end, end_time[obj.i][obj.j-1])
                end = start + prepare + work
                temp_start.append(start)
                temp_end.append(end)
        best = min(temp_end)
        index = temp_end.index(best)
        obj.end = best
        if obj.k == 0:
            end_time[obj.i].append(best)
        obj.start = temp_start[index]
        schedule[obj.j][index].append(obj)
        count += 1
        # print(obj.i, obj.j, obj.k)
        end_time[obj.i][obj.j] = max(best, end_time[obj.i][obj.j])

    finish_time = 0
    for i in range(len(end_time)):
        # print(end_time[i])
        finish_time = max(finish_time, end_time[i][-1])
    z = 1/finish_time*1000000
    del end_time[:]
    return schedule, z

