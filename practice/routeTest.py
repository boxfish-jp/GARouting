import random
from deap import base, creator, tools, algorithms

# 最大化問題として設定
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# 個体の定義（list型と指定しただけで、中身の遺伝子は後で入れる）
creator.create("Individual", list, fitness=creator.FitnessMin)

AreaSize = [30, 30]
GoalPos = [30, 30]
gemNum = 100


# 現在位置の計算
def calcInst(indi: int):
    match indi:
        case 0:
            return [0, 1]
        case 1:
            return [1, 0]
        case 2:
            return [0, -1]
        case 3:
            return [-1, 0]

    raise ValueError("indi is not in range 0-3", indi)


def encodeRoute(individual):
    for i in individual:
        if i < 0 or i > 3:
            print("individual is not in range 0-3:", i)
    step = 1
    position = [[0, 0]]
    nearest = GoalPos[0] + GoalPos[1]
    for indi in individual:
        inst = calcInst(indi)
        position.append(
            [position[step - 1][0] + inst[0], position[step - 1][1] + inst[1]]
        )

        if position[step] == GoalPos:
            return (step, position)

        if (
            position[step][0] < 0
            or position[step][0] > AreaSize[0]
            or position[step][1] < 0
            or position[step][1] > AreaSize[1]
        ):
            if step == gemNum:
                return (10000, position)
            return ((gemNum - step) * 10000, position)

        distance = abs(position[step][0] - GoalPos[0]) + abs(
            position[step][1] - GoalPos[1]
        )
        if distance < nearest:
            nearest = distance

        step += 1

    return (nearest * gemNum, position)


# 経路の評価関数
def evalRoute(individual):
    encode = encodeRoute(individual)
    return (encode[0],)


def MakeRand():
    while True:
        rand = random.randint(0, 3)
        if rand >= 0 and rand <= 3:
            return rand
        print("rand is not in range 0-3:", rand)


toolbox = base.Toolbox()
toolbox.register("attribute", MakeRand)
toolbox.register(
    "individual", tools.initRepeat, creator.Individual, toolbox.attribute, gemNum
)
# 集団の個体数を設定するための関数を準備
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
# トーナメント方式で次世代に子を残す親を選択（tornsizeは各トーナメントに参加する個体の数）
toolbox.register("select", tools.selTournament, tournsize=5)
# 交叉関数の設定。ブレンド交叉という手法を採用
toolbox.register("mate", tools.cxTwoPoint)
# 突然変異関数の設定。indpbは各遺伝子が突然変異を起こす確率。変異は0~20の整数で変異
toolbox.register("mutate", tools.mutUniformInt, low=0, up=3, indpb=0.2)
# 評価したい関数の設定（目的関数のこと）
toolbox.register("evaluate", evalRoute)


# 何世代まで行うか
NGEN = 100
# 集団の個体数
POP = 80
# 交叉確率
CXPB = 0.9
# 個体が突然変異を起こす確率
MUTPB = 0.01

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
print("最も良い個体は %sで、そのときの目的関数の値は %s" % (encodeRoute(best_ind), best_ind.fitness.values))
