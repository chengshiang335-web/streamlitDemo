import streamlit as st
import pandas as pd
from  numpy.random import default_rng as rnd
import streamlit as st
import pandas as pd


df = pd.DataFrame(rnd().random((30, 3)), columns=['a', 'b', 'c'])

st.header("Line Chart Demo")
st.subheader("各業務業績")
st.line_chart(df)

