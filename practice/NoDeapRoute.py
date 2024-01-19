import random
import copy

genLen = 15  # 経路の長さ
AreaSize = [5, 5]
GoalPos = [4, 4]
start = [0, 0]
NGEN = 30  # 世代数
POP = 1000  # 集団の数


# 現在位置の計算
def makeInst():
    rand = random.randint(0, 3)
    match rand:
        case 0:
            return [0, 1]
        case 1:
            return [1, 0]
        case 2:
            return [0, -1]
        case 3:
            return [-1, 0]

    raise ValueError("rand is not in range 0-3", rand)


# 進むノードの選択
def selectNode(lastNode: list[int]):
    while True:
        Inst = makeInst()
        nextNode = [lastNode[0] + Inst[0], lastNode[1] + Inst[1]]
        if (
            nextNode[0] < 0
            or nextNode[0] > AreaSize[0]
            or nextNode[1] < 0
            or nextNode[1] > AreaSize[1]
        ):
            continue
        else:
            return nextNode


# 経路の初期生成
def makeIndividual():
    route: list[list[int]] = []
    route.append(start)
    for i in range(0, genLen - 1):
        nextNode = selectNode(route[i])
        route.append(nextNode)

    return route


# 経路の評価関数
def evalRoute(individual: list[list[int]]):
    cleanIndividual: list[list[int]] = []  # 到達後のノードを削除した経路
    for i in range(0, len(individual)):
        cleanIndividual.append(individual[i])
        if individual[i] == GoalPos:
            return (i, cleanIndividual)

    lastNode = cleanIndividual[len(cleanIndividual) - 1]
    cost = abs(GoalPos[0] - lastNode[0]) + abs(GoalPos[1] - lastNode[1])
    return (cost * len(cleanIndividual) * 10, cleanIndividual)


# 初期世代の生成
def makePopulation():
    population = []
    for i in range(0, POP):
        population.append(makeIndividual())

    return population


# 選択関数
def select_roulette(population):
    """
    selected = []
    weights = []
    max = 0
    for indi in population:
        weights.append(evalRoute(indi)[0])
        if max < weights[-1]:
            max = weights[-1]

    for i in range(0, len(population)):
        weights[i] = max - weights[i] + 1

    selected = random.choices(population, weights=weights, k=len(population))

    print("selected", selected)
    return selected
    """
    sortArray = sorted(population, key=lambda x: evalRoute(x)[1])
    # sortArrayを半分に分ける
    quote = len(sortArray) // 4
    first_quote = sortArray[:quote]
    second_quote = sortArray[quote : quote * 2]
    third_quote = sortArray[quote * 2 : quote * 3]
    forth_quote = sortArray[quote * 3 :]

    # それぞれランダムに並び替える
    random.shuffle(first_quote)
    random.shuffle(second_quote)
    random.shuffle(third_quote)
    random.shuffle(forth_quote)

    # 2つの配列を結合する
    result = first_quote + second_quote + third_quote + forth_quote
    return result


# ノードが重複または、ノードが隣接しているかを確認する
def checkNearBy(individual1: list[list[int]], individual2: list[list[int]]):
    for ind in range(len(individual1) // 2):
        i = random.randint(len(individual1) // 4, len(individual1) // 4 * 3)
        for j in range(len(individual2) // 4, len(individual2) // 4 * 3):
            if individual1[i] == individual2[j]:
                # print(individual1[i])
                return individual1[i]

            if individual1[i] == individual2[j] or individual1[i] == individual2[j]:
                return (individual1[i], individual1[i])
    return False


# 交叉関数
def crossover(individualM: list[list[int]], individualD: list[list[int]]):
    checker = checkNearBy(individualM, individualD)

    if checker == False:
        return False
    elif type(checker) == list:
        # print("m:\n", individualM)
        # print("d\n", individualD)
        indexM = individualM.index(checker)
        indexD = individualD.index(checker)
        # print("indexM", indexM)
        # print("indexD", indexD)
        chilid1 = evalRoute(individualM[:indexM] + individualD[indexD:])[1]
        chilid2 = evalRoute(individualD[:indexD] + individualM[indexM:])[1]
        return (chilid1, chilid2)
    elif type(checker) == tuple:
        print("m:\n", individualM)
        print("d\n", individualD)
        index1 = individualM.index(checker[0])
        index2 = individualD.index(checker[1])
        chilid1 = evalRoute(individualM[: index1 + 1] + individualD[index2:])[1]
        chilid2 = evalRoute(individualD[: index2 + 1] + individualM[index1:])[1]
        return (chilid1, chilid2)

    raise ValueError("checker is", checker)


# 半分より上位の個体同士で交叉
def MakeSmartChildren(selected: list, length: int):
    children = []
    for j in range(0, length // 4):
        for k in range(length // 4, length // 2):
            if j == k:
                continue
            child = crossover(selected[j], selected[k])
            if child != False:
                # print("j", j)
                # print("k", k)
                if child[0] not in children:
                    children.append(child[0])
                if child[1] not in children:
                    children.append(child[1])

            if len(children) >= length:
                # print("children", len(children))
                # print("population", len(population))
                # print("full")
                return children.copy()

    return children.copy()


# 全ての個体について交叉
def MakeChildren(selected: list, length: int, rest: int):
    children = []
    # 残りの個体も交叉
    for j in range(length // 2, length // 4 * 3):
        for k in range(length // 4 * 3, length):
            if j == k:
                continue
            child = crossover(selected[j], selected[k])
            if child != False:
                if child[0] not in children:
                    children.append(child[0])
                if child[1] not in children:
                    children.append(child[1])

            if len(children) >= rest:
                return children.copy()

    return children.copy()


# 一番成績の良い個体を出力する
def printBest(population):
    best = population[0]
    for i in range(0, len(population)):
        if evalRoute(population[i])[0] < evalRoute(best)[0]:
            best = population[i]

    print("score", evalRoute(best)[0])
    # print(evalRoute(best)[1])


# メイン処理
def main():
    population = makePopulation()
    for i in range(0, NGEN):
        children = []
        selected = select_roulette(population)
        index = 0
        # 半分より上位の個体同士で交叉
        smartChild = MakeSmartChildren(selected, len(population))
        for child in smartChild:
            children.append(child)

        # 　残りに必要な個体数を計算
        rest = len(population) - len(children)
        # 残りの個体も交叉

        if rest > 0:
            restChild = MakeChildren(selected, len(population), rest)
            for child in restChild:
                children.append(child)
        # print("children", children)
        # print("population", population)

        population = copy.deepcopy(children)
        # print("len", len(population))
        # for popu in population:
        # print("1:", popu)

        print("children", len(children))
        printBest(population)


main()
