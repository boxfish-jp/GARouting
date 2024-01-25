import numpy as np
import json

# 2行2列のランダムな整数値の配列を作成（例：0から9の範囲）
random_array = np.random.randint(3, size=(17, 17))
print("[")
for i in range(len(random_array)):
    random_array[i][i] = 0
    obj = json.dumps(random_array[i].tolist()) + ","
    print(obj)

print("]")
