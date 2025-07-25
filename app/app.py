import streamlit as st
import pandas as pd
from models import (
    Controller, Database, Construct
)
import tempfile

import random

# Kết nối MongoDB
connect_string = 'mongodb://localhost:27017/'
db_name = 'vocab_app'
collection_name = 'dictionary'

database = Database(connect_string, db_name)
controller = Controller(database, collection_name)

st.header("📤 Upload file txt để đẩy vào database")

uploaded_file = st.file_uploader("Chọn file .txt", type=["txt"])

if uploaded_file is not None:
    # Lưu file tạm thời để truyền path cho Construct
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    if st.button("🚀 Đẩy vào MongoDB"):
        try:
            constructor = Construct(tmp_path, database, collection_name)
            constructor.push_into_database()
            st.success("✅ Đã thêm dữ liệu vào MongoDB!")
        except Exception as e:
            st.error(f"❌ Lỗi khi thêm dữ liệu: {e}")


# ==== PHẦN 1: Hiển thị từ vựng ngẫu nhiên ====
st.title("📚 Từ vựng ngẫu nhiên")
st.write("Nhập số lượng từ muốn lấy và nhấn nút:")

col1, col2 = st.columns([2, 1])
with col1:
    num_words = st.number_input("Số từ muốn lấy", min_value=1, max_value=100, value=5, step=1)
with col2:
    run_button = st.button("🎲 Lấy từ")

if run_button:
    try:
        documents, _ = controller.get_random_documents(num_words)
        table_data = []
        for doc in documents:
            table_data.append({
                "Word": doc.get("word", ""),
                "Meaning": doc.get("definition", ""),
                "Types": doc.get("types", "")
            })

        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Lỗi: {e}")
# ==== PHẦN 2: Trắc nghiệm từ vựng ====
st.header("🧠 Trắc nghiệm từ vựng")

# Khởi tạo số câu hỏi (mặc định 5)
num_qs = st.number_input("Chọn số câu hỏi muốn làm", min_value=1, max_value=50, value=5, step=1)

# Nút bắt đầu
if st.button("🚀 Bắt đầu bài trắc nghiệm mới"):
    st.session_state.questions = controller.mutiple_questions(num_qs)
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.rerun()

# Kiểm tra nếu đã có câu hỏi trong session
if "questions" in st.session_state:
    questions = st.session_state.questions
    q_index = st.session_state.q_index

    if q_index < len(questions):
        q = questions[q_index]
        st.subheader(f"Câu hỏi {q_index + 1} / {len(questions)}: {q['word']}")
        selected = st.radio("Chọn nghĩa đúng:", q['options'], key=f"question_{q_index}")

        if st.button("🔍 Kiểm tra"):
            if selected == q["correct_ans"]:
                st.success("✅ Chính xác!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Sai rồi! Đáp án đúng là: {q['correct_ans']}")

        if st.button("➡️ Câu tiếp theo"):
            st.session_state.q_index += 1
            st.rerun()
    else:
        st.success(f"🎉 Bạn đã hoàn thành! Điểm số: {st.session_state.score}/{len(questions)}")
        if st.button("🔁 Làm lại"):
            st.session_state.questions = controller.mutiple_questions(num_qs)
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.rerun()
else:
    st.info("⬅️ Vui lòng chọn số câu hỏi và bấm **Bắt đầu** để làm bài trắc nghiệm.")
