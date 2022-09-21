import os
import pandas as pd
import ujson as json
from aggregates import aggregate_findmax, aggregate_sum7to3, mapping_7to3, mapping_customize
from aggregates import S_NTL, S_NEG, S_POS


class LabelLoader:
    def __init__(self,
                 dir: str,
                 csvfile: str = "Labels.csv"):
        # check if dir exists
        assert (os.path.exists(dir))
        csv_path = os.path.join(dir, csvfile)
        # check is exists Labels.csv
        assert (os.path.exists(csv_path) and os.path.isfile(csv_path))
        data = pd.read_csv(csv_path)

        self.filenames = list(map(lambda x: os.path.splitext(x),
                                  list(data["Filename"])))
        self.labels = list(data["Label"])

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, item):
        ext = None
        if type(item) == tuple:
            id, ext = item
        else:
            id = item
        assert (0 <= id < len(self))
        if ext is not None:
            return self.filenames[id][0] + ext, self.labels[id]
        else:
            return "".join(self.filenames[id]), self.labels[id]


DATA_PATH = os.path.join(".", "data")
RUN_PATH = os.path.join(".", "run")


def get_run(year: int = 2019, MTCNN: bool = False) -> str:
    assert (year in (2019, 2020))
    affix = "MTCNN" if MTCNN else "Default"
    folder_name = f"{year}_{affix}"
    folder_path = os.path.join(RUN_PATH, folder_name)
    assert (os.path.exists(folder_path))
    return folder_path


def get_label(year: int = 2019) -> LabelLoader:
    assert (year in (2019, 2020))
    path = os.path.join(DATA_PATH, str(year))
    assert (os.path.exists(path))
    return LabelLoader(path)


if __name__ == "__main__":
    year = 2020
    use_MTCNN = False

    label_loader = get_label(year)
    run_path = get_run(year, use_MTCNN)

    def extractor(affix, frame):
        result = {}
        for key in ("angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"):
            result[key] = frame[f"{key}{affix}"]
        return result

    # 方法0，suprise映射为positive
    # handlers = [aggregate_findmax, lambda dat: mapping_7to3(dat, S_POS)]

    # 方法1，suprise映射为negative
    # handlers = [aggregate_findmax, lambda dat: mapping_7to3(dat, S_NEG)]

    # 方法2，suprise映射为neutral
    # handlers = [aggregate_findmax, lambda dat: mapping_7to3(dat, S_NTL)]

    # 方法3，先加（suprise映射为negative），再映射
    # handlers = [lambda dat: aggregate_sum7to3(dat, S_NEG), aggregate_findmax]

    # 方法4，先加（suprise映射为neutral），再映射
    # handlers = [lambda dat: aggregate_sum7to3(dat, S_NTL), aggregate_findmax]

    # 方法5，先加（suprise映射为positive），再映射
    # handlers = [lambda dat: aggregate_sum7to3(dat, S_POS), aggregate_findmax]

    handlers = [aggregate_findmax,
                lambda dat: mapping_customize(dat, angry=S_NEG, disgust=S_NEG, fear=S_NTL, sad=S_NTL, happy=S_POS, surprise=S_POS, neutral=S_NTL)]

    # out = []
    total = 0
    ok = 0
    print("filename\tpredict\tgolden\tpositive count\tnegative count\tneutral count")
    for idx in range(len(label_loader)):
        filename, golden_label = label_loader[idx, ".txt"]
        merged_path = os.path.join(run_path, filename)
        with open(merged_path, 'r') as fopen:
            json_data = json.load(fopen)
        # 首先遍历每一个帧
        result_count = {}
        for frame in json_data:
            # 每一个帧里面，可能就有多个脸。
            # 我们打算只处理第一张脸，后面的脸全部删除。
            face_cnt = 0
            if "box0" not in frame:
                continue
            cur_face_data = extractor(0, frame)
            for handler in handlers:
                cur_face_data = handler(cur_face_data)
            for key in cur_face_data.keys():
                result_count[key] = result_count.get(key, 0) + 1
                break
        best_key = None
        best_value = 0
        for key, value in result_count.items():
            if value > best_value:
                best_key = key
                best_value = value
        if best_key is None:
            continue

        # out.append({
        #     "filename": filename,
        #     "golden": golden_label,
        #     "predict": best_key,
        #     "predicts": result_count
        # })
        print(f"{filename}\t{best_key}\t{golden_label}\t{result_count.get(S_POS,0)}\t{result_count.get(S_NEG,0)}\t{result_count.get(S_NTL,0)}")
        total += 1
        if golden_label == best_key:
            ok += 1

    print("========================")
    print("accuracy: {0:.2f}%".format(ok / total * 100))