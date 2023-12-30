import sqlite3
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

from streamlit_searchbox import st_searchbox

from utils import check_folder_existance, filtered_search_vocabolario

# Check folders exists
check_folder_existance()

st.set_page_config(
    page_title="Dizionario",
    page_icon="📖 Dizionario Italiano Bivongese",
)

st.title('Vocabolario Italiano-Bivongese')

selected_value = st_searchbox(
    filtered_search_vocabolario,
    key="vocab_searchbox"
)

if selected_value is not None:
    st.subheader("Vocabolo trovato")
    st.markdown(f"*Termine Italiano*: ***{selected_value.it_term}***.")
    st.markdown(f"*Termine Bivongese*: ***{selected_value.biv_term}***.")
    st.audio(data=str(selected_value.audio_path), format=f"audio/{str(selected_value.audio_path).split('.')[-1]}")
    

