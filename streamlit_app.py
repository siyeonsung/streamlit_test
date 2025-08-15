# streamlit.run streamlit_app.py

import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.title("pycon tutorial")
st.info(
    "파이콘 튜토리얼 예제"
)

st.subheader("첫 번째 앱")

st.image("https://static.streamlit.io/examples/cat.jpg", caption="귀여운 고양이", use_container_width=True)


