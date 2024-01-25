import array
import random
import json
import matplotlib.pyplot as plt
import numpy
import time

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

# gr*.json contains the distance map in list of list style in JSON format
# Optimal solutions are : gr17 = 2085, gr24 = 1272, gr120 = 6942

with open("C:/Users/boxfi/OneDrive/デスクトップ/GARouting/conf5.json", "r") as tsp_data:
    tsp = json.load(tsp_data)


distance_map = tsp["DistanceMatrix"]
confusion_map = tsp["confusionMatrix"]
init_distance_map = tsp["initDistance"]
init_confusion_map = tsp["initConfusion"]
IND_SIZE = tsp["TourSize"]

# 問題の最適化のための型定義
# 最小化問題として定義
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# 遺伝子型の定義(配列型であり、配列内の型はint型)
creator.create("Individual", array.array, typecode="i", fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
# 0~IND_SIZE-1までの整数をランダムに並べたリストを生成する関数を登録
toolbox.register("indices", random.sample, range(IND_SIZE), IND_SIZE)

# Structure initializers
# initItrateはindices関数を単に呼び出すだけの関数
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
# initRepeatは第一引数で指定した関数を第二引数で指定した回数呼び出す関数,今回は第2引数は後で入れる
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evalTSP(individual):
    distance = init_distance_map[individual[0]] * (init_confusion_map[0][individual[0]])
    distance += init_distance_map[individual[-1]] * (
        init_confusion_map[1][individual[-1]]
    )
    i = 0
    for gene1, gene2 in zip(individual[0:-1], individual[1:]):
        distance += distance_map[gene1][gene2] * (confusion_map[i][gene1][gene2])
        i += 1
    return (distance,)


"""
zip関数について
zip([a, b, c], [x, y, z]) == [(a, x), (b, y), (c, z)]
"""

toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evalTSP)


def main():
    # random.seed(169)
    start_time = time.time()

    pop = toolbox.population(n=10)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    # logbook = tools.Logbook()
    # logbook.header = ["gen", "nevals"] + (stats.fields if stats else [])
    pop, log = algorithms.eaSimple(
        pop, toolbox, 0.7, 0.2, 10, stats=stats, halloffame=hof
    )
    """
    # プロットの作成
    gen = log.select("gen")
    min = log.select("min")
    plt.plot(gen, min)
    plt.xlabel("Generation")
    plt.ylabel("Min Fitness")
    plt.show()
    """
    end_time = time.time()  # 終了時間
    print("Execution time: ", end_time - start_time, "seconds")  # 実行時間の表示
    return pop, stats, hof


if __name__ == "__main__":
    main()
