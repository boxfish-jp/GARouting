import itertools
import time
from pickMatrix import pickMatrix

start_time = time.time()  # 開始時間
# 0~4の値が入った配列
array = range(5)

# すべての並べ替えを生成
permutations = list(itertools.permutations(array))

# 並べ替えを出力
for perm in permutations:
    print(perm)

pick = [0, 1, 2, 3, 4, 19]

maps = pickMatrix(pick)
init_distance_map = maps["initDistance"]
init_confusion_map = maps["initConfusion"]
distance_map = maps["DistanceMatrix"]
confusion_map = maps["confusionMatrix"]
rankCity = maps["rankCity"]
print(maps)


def evalTSP(individual):
    distance = init_distance_map[individual[0]] * (init_confusion_map[0][individual[0]])
    distance += init_distance_map[individual[-1]] * (
        init_confusion_map[1][individual[-1]]
    )
    i = 0
    for gene1, gene2 in zip(individual[0:-1], individual[1:]):
        distance += distance_map[gene1][gene2] * (confusion_map[i][gene1][gene2])
        i += 1
    return distance


result = []
for individual in permutations:
    result.append(evalTSP(individual))

min = 1000000
index = 0
i = 0
for cost in result:
    if cost < min:
        min = cost
        index = i
    i += 1

print("最小値は" + str(min) + "で、その時の順番は" + str(permutations[index]), end="")
for i in permutations[index]:
    print(" -> " + rankCity[pick[i + 1]], end="")
end_time = time.time()  # 終了時間
print("Execution time: ", end_time - start_time, "seconds")  # 実行時間の表示
