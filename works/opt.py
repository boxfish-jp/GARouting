import itertools
import json


import itertools


def tsp_dynamic_programming(distances):
    n = len(distances)

    # dp[mask][pos]は、maskが含む都市の集合でposの都市にいるときの最小コスト
    dp = [[float("inf")] * n for _ in range(1 << n)]

    # 初期条件: 出発点から出発点へのコストは0
    dp[1][0] = 0

    for mask in range(1, 1 << n):
        for pos in range(n):
            if (mask >> pos) & 1:  # maskにposが含まれている場合
                for prev in range(n):
                    if (
                        mask >> prev
                    ) & 1 and prev != pos:  # maskにprevが含まれていて、prevとposが異なる場合
                        dp[mask][pos] = min(
                            dp[mask][pos],
                            dp[mask ^ (1 << pos)][prev] + distances[prev][pos],
                        )

    # 最後に出発点に戻るコストを求める
    mask = (1 << n) - 1
    min_cost = min(dp[mask][pos] + distances[pos][0] for pos in range(1, n))

    return min_cost


with open(
    "C:/Users/boxfi/OneDrive/デスクトップ/GARouting/works/conf17.json", "r"
) as tsp_data:
    tsp = json.load(tsp_data)


distance_map = tsp["DistanceMatrix"]
confusion_map = tsp["confusionMatrix"]
IND_SIZE = tsp["TourSize"]

cost = [[]]
for i in range(IND_SIZE):
    if i != IND_SIZE - 1:
        cost.append([])
    for j in range(IND_SIZE):
        cost[i].append(distance_map[i][j] * (confusion_map[i][j] + 1))
# print(cost)
# 厳密解の計算
optimal_cost = tsp_dynamic_programming(cost)
print("Optimal Cost:", optimal_cost)
