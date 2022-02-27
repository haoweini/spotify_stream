import streamlit as st
from data.get_saved_library import get_saved_library

# Title at the top of the application 
st.title('Spotify Stream')

df = get_saved_library()

st.table(df)