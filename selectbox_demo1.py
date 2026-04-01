import streamlit as st

lang = st.selectbox("請選擇: ", ("Java", "Python", "C#", "JavaScript"))

st.write(f"挑選了 {lang}")

def selectOption():
    st.write(f"改變了選項2的內容 {st.session_state.o2item}")

st.selectbox("選項2", 
             ("Power BI", "DAX", "Power Query") , 
             #觸發時間: 當 使用者改變選項時 會觸發 selectOption執行
             on_change=selectOption,
             #綁定 獨一值, 系統有一個特殊的儲存庫(st.session_state)會存放這些 key(變數)的值
             key="o2item"
             )


