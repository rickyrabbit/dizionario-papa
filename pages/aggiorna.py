from pathlib import Path
from typing import List
import streamlit as st

from streamlit_searchbox import st_searchbox
# from utils import ALLOWED_AUDIO_EXT, aggiornaVocabolo, creaVocabolo, salvaFileAudio, salvaRegistrazioneAudio
from utils import form_aggiorna_vocabolo, search_vocabolario

# function with list of labels

# pass search function to searchbox
selected_value = st_searchbox(
    search_vocabolario,
    key="vocab_searchbox"
)

edit_instance = st.empty()



    
st.session_state.is_mic_recording: bool = False

if selected_value is not None:
    with edit_instance.container():
        
        st.session_state.is_mic_recording: bool = False
        st.header("Aggiorna vocabolo")
        form_aggiorna_vocabolo(vocabolo=selected_value)
else:
    edit_instance.empty()