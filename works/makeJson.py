import numpy as np
import json

# 2行2列のランダムな整数値の配列を作成（例：0から9の範囲）
random_array = np.random.uniform(1, 2, size=(20, 20))

# 配列の各要素を丸める
random_array = np.around(random_array, 2)
print("[")
for i in range(7):
    print("[")
    for t in range(len(random_array)):
        random_array[i][i] = 0
        obj = json.dumps(random_array[t].tolist()) + ","
        print(obj)
    print("],")

print("]")
