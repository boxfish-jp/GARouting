# 個体の各遺伝子を決めるために使用
import random

# DEAPの中にある必要なモジュールをインポート
from deap import base
from deap import creator
from deap import tools
from deap import algorithms

# 最大化問題として設定
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
# 個体の定義（list型と指定しただけで、中身の遺伝子は後で入れる）
creator.create("Individual", list, fitness=creator.FitnessMax)
# 各品物の（重さ,価値）をitemsに格納
items = {}
items[0] = (5, 110)
items[1] = (10, 140)
items[2] = (9, 150)
items[3] = (5, 130)
items[4] = (5, 110)
items[5] = (4, 90)


# 目的関数の定義。#必ずreturnの後に,をつける
# 個体は(1,3,0,2,4,3)などであり、総価値と総重量を計算します。
# 重量が100を超えてはいけないので、100を超えた場合、価値を0にします。
def evalKnapsack(individual):
    weight = 0.0
    value = 0.0
    for i in range(6):
        weight += items[i][0] * individual[i]
        value += items[i][1] * individual[i]
    if weight > 100:
        value = 0.0
    return (value,)


constArray = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
letArray = []


def makeRand():
    global letArray
    if len(letArray) == 0:
        letArray = constArray
    rand = random.choice(letArray)
    # letArray.remove(rand)
    return rand


# 各種関数の設定を行います
toolbox = base.Toolbox()
# random.uniformの別名をattribute関数として設定。各個体の遺伝子の中身を決める関数(各遺伝子は0～10のランダムな整数)
toolbox.register("attribute", makeRand)
# individualという関数を設定。それぞれの個体に含まれる6個の遺伝子をattributeにより決めるよ、ということ。
toolbox.register(
    "individual", tools.initRepeat, creator.Individual, toolbox.attribute, 6
)
# 集団の個体数を設定するための関数を準備
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
# トーナメント方式で次世代に子を残す親を選択（tornsizeは各トーナメントに参加する個体の数）
toolbox.register("select", tools.selTournament, tournsize=5)
# 交叉関数の設定。一点交叉を採用
toolbox.register("mate", tools.cxOnePoint)
# 突然変異関数の設定。indpbは各遺伝子が突然変異を起こす確率。変異は0~20の整数で変異
toolbox.register("mutate", tools.mutUniformInt, low=0, up=20, indpb=0.2)
# 評価したい関数の設定（目的関数のこと）
toolbox.register("evaluate", evalKnapsack)
# 乱数の固定
random.seed(128)
# 何世代まで行うか
NGEN = 50
# 集団の個体数
POP = 80
# 交叉確率
CXPB = 0.9
# 個体が突然変異を起こす確率
MUTPB = 0.1
# 集団は80個体という情報の設定
pop = toolbox.population(n=POP)
# 集団内の個体それぞれの適応度（目的関数の値）を計算
for ind in pop:
    ind.fitness.values = toolbox.evaluate(ind)
# パレート曲線上の個体(つまり、良い結果の個体)をhofという変数に格納
hof = tools.ParetoFront()
# 最も単純なSimple GAという進化戦略を採用
algorithms.eaSimple(pop, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN, halloffame=hof)
# 最終的な集団(pop)からベストな個体を1体選出する関数
best_ind = tools.selBest(pop, 1)[0]
# 結果表示
print("最も良い個体は %sで、そのときの目的関数の値は %s" % (best_ind, best_ind.fitness.values))
