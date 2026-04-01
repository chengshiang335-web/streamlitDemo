import streamlit as st
#製作 sidebar 版面

lang = st.sidebar.selectbox("個人專長介紹: ", ("Power BI", "Python", "SQL", "DAX"))

#一次放入多個
with st.sidebar:
    st.subheader("以下是我個人作品介紹")
    st.divider()
    st.selectbox("作品介紹", ("電子商務分析","台中市近年溫濕度變化分析"))
    st.divider()
    
# 非 sidebar 代表就是主要畫面
st.title("這裡是主要的 Main Content")

match lang:
    case "Power BI":
        st.subheader("你挑選 Power BI")
    case "Python":
        st.subheader("你挑選 Python + Streamlit 作品在這")
    case "SQL":
        st.subheader("你挑選 SQL") 