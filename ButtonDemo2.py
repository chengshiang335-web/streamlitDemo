import streamlit as st
import pandas as pd

st.title("Button Demo")


msgs = ""

def open_csv():
    st.write("你按了Button3 (開啟CSV檔案)")
    df = pd.read_csv("./assets/Amazon Customer Behavior Survey.csv")
    st.dataframe(df)
    global msgs
    msgs += "你按了Button3 (開啟CSV檔案)\n"

click1 = st.button("這是Button1", key="btn1",type="primary",icon="👓")
click2 = st.button("這是Button2", key="btn2",type="secondary",icon="🥽")
click3 = st.button("這是Button3", key="btn3",type="primary",icon="🧑",on_click=open_csv)

st.write("這是ButtonDemo2.py")
if click1:
    st.write("你按了Button1")
if click2:
    st.write("你按了Button2")
        
