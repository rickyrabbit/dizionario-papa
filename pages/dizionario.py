import sys
sys.path.append("..")

import streamlit as st
from model import  get_transcriptions

st.header("Lista dei vocaboli")
transcription_list = get_transcriptions()
vocab_ita_col, vocab_trad_col, vocab_audio_col = st.columns(3)

with vocab_ita_col:
    st.subheader("italiano")

with vocab_trad_col:
    st.subheader("bivongese")

with vocab_audio_col:
    st.subheader("audio")

st.divider()
for tr in transcription_list:
    with st.container():
        vocab_ita_col, vocab_trad_col, vocab_audio_col = st.columns(3)

        with vocab_ita_col:
            st.markdown(f"***{str(tr.it_term)}***")

        with vocab_trad_col:
            st.markdown(f"***:red[{str(tr.biv_term)}]***")

        with vocab_audio_col:
            st.audio(data=str(tr.audio_path),format=f"audio/{str(tr.audio_path).split('.')[-1]}")
        