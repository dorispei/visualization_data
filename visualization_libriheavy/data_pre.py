import json
from pathlib import Path


# spk=0
# # 输入文件路径
# emo_file = f"/home/v-hanchenpei/valleblob/v-hanchenpei/data/download/librilight/cases_and_punc/data/wav_segments/batch_lists_new/batch_emo2vect_{spk:04d}.txt"
# trans_file = f"/home/v-hanchenpei/valleblob/v-hanchenpei/data/download/librilight/cases_and_punc/data/wav_segments/batch_lists_new/batch_trans_{spk:04d}.txt"

# # 输出 JSON 文件
# output_json = f"./visualization/batch_data_{spk:04d}.json"

# # audio_path 前缀
# prefix = "/home/v-hanchenpei/valleblob/v-hanchenpei/data/download/librilight/cases_and_punc/data/wav_segments/forced_align_wavs/"

# # -----------------------------
# # 读取 transcription 文件
# # -----------------------------
# trans_dict = {}
# with open(trans_file, "r", encoding="utf-8") as f:
#     for line in f:
#         line = line.strip()
#         if not line:
#             continue
#         parts = line.split(maxsplit=1)
#         if len(parts) != 2:
#             continue
#         audio_path, transcription = parts
#         trans_dict[audio_path] = transcription

# # -----------------------------
# # 读取 emotion 文件，并合并 transcription
# # -----------------------------
# data = []
# with open(emo_file, "r", encoding="utf-8") as f:
#     for line in f:
#         line = line.strip()
#         if not line:
#             continue
#         parts = line.split(maxsplit=3)  # audio_path emotion max_prob problist
#         if len(parts) < 3:
#             continue
#         audio_path_raw, emotion, max_prob = parts[:3]

#         # 拼接前缀
#         audio_path_full =  audio_path_raw.replace("/datablob","/home/v-hanchenpei/valleblob")
#         audio_path_raw = "/".join(audio_path_full.split("/")[-3:])

#         # 获取 transcription
#         transcription = trans_dict.get(audio_path_raw, "")

#         item = {
#             "audio_path": audio_path_full,
#             "transcription": transcription,
#             "emotion": emotion,
#             "max_prob": float(max_prob)
#         }
#         data.append(item)

# # -----------------------------
# # 保存 JSON
# # -----------------------------
# with open(output_json, "w", encoding="utf-8") as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)

# print(f"已生成 {len(data)} 条记录，保存到 {output_json}")

# import os
# import json

# # 你的音频目录
# root_dir = "/home/v-hanchenpei/valleblob/v-hanchenpei/data/download/librilight/cases_and_punc/data/wav_segments/forced_align_wavs/14/"

# # 输出 JSON 文件路径
# output_json = "./visualization/data/audio_paths.json"

# # 获取所有 .wav 文件的绝对路径
# audio_list = []
# audio_list = []

# # 递归遍历所有子目录
# for dirpath, dirnames, filenames in os.walk(root_dir):
#     for filename in filenames:
#         if filename.lower().endswith(".wav"):
#             abs_path = os.path.abspath(os.path.join(dirpath, filename))
#             audio_list.append({"audio_path": abs_path})

# # 保存到 JSON
# with open(output_json, "w", encoding="utf-8") as f:
#     json.dump(audio_list, f, ensure_ascii=False, indent=4)

# print(f"已找到 {len(audio_list)} 个音频文件，保存到 {output_json}")

import json

# 原始 json 文件
input_json = "/home/v-hanchenpei/valleblob/v-hanchenpei/data/download/librilight/cases_and_punc/data/wav_segments/batch_lists_new/filtered_mfa_large_info_all.json"
output_json = "./visualization/data/filtered_large.json"

with open(input_json, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

processed_data = []

for audio_path, info in raw_data.items():
    item = {
        "audio_path": audio_path,
        "speaker_id": info.get("speaker_id", "unknown"),
        "transcription": info.get("transcription", ""),
        "emotion": info.get("emotion_classification", "unknown"),
        "max_prob": float(info.get("emotion_max_prob", 0.0)),
        "energy_cate": info.get("energy_category", ""),
        "pitch_cate": info.get("pitch_category", ""),
        "speed_cate": info.get("speed_category", ""),
        "pitch_std_cate": info.get("pitch_std_category", ""),
        "uid": info.get("uni_id")
    }
    processed_data.append(item)

with open(output_json, "w", encoding="utf-8") as f:
    json.dump({"data": processed_data}, f, ensure_ascii=False, indent=2)