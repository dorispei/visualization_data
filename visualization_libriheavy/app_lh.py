import streamlit as st
import json
import os

from azure.storage.blob import BlobClient
sas_token = r"sv=2023-01-03&spr=https%2Chttp&st=2025-08-19T08%3A08%3A32Z&se=2025-08-20T08%3A08%3A32Z&skoid=3b3c6740-2dac-4874-ae17-538255627874&sktid=72f988bf-86f1-41af-91ab-2d7cd011db47&skt=2025-08-19T08%3A08%3A32Z&ske=2025-08-20T08%3A08%3A32Z&sks=b&skv=2023-01-03&sr=c&sp=rlf&sig=NLHIsiO%2FKis4FIbxEl7BrpiiMLoOpDdWSbLHW%2FvkU8w%3D"

# ---------------------------
# 页面配置
# ---------------------------
st.set_page_config(page_title="音频数据可视化", layout="wide")

# ---------------------------
# 输入 JSON 文件路径
# ---------------------------
st.title("🎧 音频数据可视化工具")

json_path = st.text_input("输入 JSON 文件路径", "./visualization_libriheavy/data/filtered_large.json")

@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"文件不存在: {file_path}")
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and "data" in data:
                data = data["data"]
            if not isinstance(data, list):
                st.error("JSON 文件必须是一个包含字典的列表")
                return None
            return data
    except Exception as e:
        st.error(f"无法解析 JSON 文件: {e}")
        return None

data = load_data(json_path)

# ---------------------------
# 筛选功能
# ---------------------------
if data:
    spk_list = sorted(set(item.get("speaker_id", "unknown") for item in data))
    emo_list = sorted(set(item.get("emotion", "unknown") for item in data))

    st.sidebar.header("筛选条件")
    selected_spk = st.sidebar.multiselect("选择 Speaker", spk_list)
    selected_emo = st.sidebar.multiselect("选择 Emotion", emo_list)

    filtered_data = [
        item for item in data
        if (not selected_spk or item.get("speaker_id") in selected_spk)
        and (not selected_emo or item.get("emotion") in selected_emo)
    ]

    st.write(f"共加载 {len(data)} 条数据，筛选后剩余 {len(filtered_data)} 条")

    # ---------------------------
    # 分页设置
    # ---------------------------
    items_per_page = 12
    total_pages = (len(filtered_data) + items_per_page - 1) // items_per_page
    page = st.number_input("选择页码", 1, max(1, total_pages), 1)

    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, len(filtered_data))

    # ---------------------------
    # 卡片式展示
    # ---------------------------
    base_path = '/home/v-hanchenpei/valleblob/v-hanchenpei/data/download/librilight/cases_and_punc/data/wav_segments/forced_align_wavs/'
    num_columns = 4
    for row_start in range(start_idx, end_idx, num_columns):
        cols = st.columns(num_columns)
        for col_idx, item in enumerate(filtered_data[row_start: row_start + num_columns]):
            with cols[col_idx]:
                st.markdown(f"**Speaker:** {item.get('speaker_id', '-')}")
                st.markdown(f"**Emotion:** {item.get('emotion', '-')}")
                st.markdown(f"**Probability:** {item.get('max_prob', '-')}")
                st.markdown(f"**Pitch:** {item.get('pitch_cate', '-')}")
                st.markdown(f"**Pitch Std:** {item.get('pitch_std_cate', '-')}")
                st.markdown(f"**Speed:** {item.get('speed_cate', '-')}")
                st.markdown(f"**energy:** {item.get('energy_cate', '-')}")
                
                st.text_area("Transcription", item.get("transcription", ""), height=80, key=f"transcription_{item['uid']}")
                url = f"https://msramcgblob.blob.core.windows.net/valle/v-hanchenpei/data/download/librilight/cases_and_punc/data/wav_segments/forced_align_wavs/{item.get('audio_path', '')}?{sas_token}"
                try:
                    blob = BlobClient.from_blob_url(url)
                
                    st.audio(blob.download_blob().readall(), format="audio/wav")
                except Exception as e:
                    st.warning("音频读取失败！")

                st.markdown("---")
else:
    st.info("请输入有效的 JSON 文件路径")
