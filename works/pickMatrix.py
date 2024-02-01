import json
from pathlib import Path


def pickMatrix(pick):
    parent = Path(__file__).parent.resolve().parent
    with open(
        parent.joinpath("works/conf.json"),
        encoding="utf-8",
        mode="r",
    ) as tsp_data:
        tsp = json.load(tsp_data)

    get_time = tsp["timeMatrix"]
    get_confusion = tsp["confusionMatrix"]

    init_distance_map = []
    for i in range(1, len(pick)):
        init_distance_map.append(get_time[pick[0]][pick[i]])

    init_confusion_map = []
    for i in range(2):
        tmp = []
        for j in range(1, len(pick)):
            tmp.append(get_confusion[i][pick[0]][pick[j]])
        init_confusion_map.append(tmp)

    distance_map = []
    for i in range(1, len(pick)):
        tmp = []
        for j in range(1, len(pick)):
            tmp.append(get_time[pick[i]][pick[j]])
        distance_map.append(tmp)

    confusion_map = []
    for i in range(5):
        tmpMat = []
        for j in range(1, len(pick)):
            tmp = []
            for k in range(1, len(pick)):
                tmp.append(get_confusion[i][pick[j]][pick[k]])
            tmpMat.append(tmp)
        confusion_map.append(tmpMat)

    return {
        "initDistance": init_distance_map,
        "initConfusion": init_confusion_map,
        "DistanceMatrix": distance_map,
        "confusionMatrix": confusion_map,
        "rankCity": tsp["rankCity"],
    }
