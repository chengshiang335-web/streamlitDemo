import streamlit as st

st.title("Button Demo")

click1 = st.button("這是Button1", key="btn1",type="primary",icon="👓")
click2 = st.button("這是Button2", key="btn2",type="secondary",icon="🥽")

if click1:
    st.write("你按了Button1")
if click2:
    st.write("你按了Button2")
        