import logging
import sys
# sys.path.append("..")

import traceback

import streamlit as st

from utils import form_nuovo_vocabolo


    
st.session_state.is_mic_recording: bool = False
form_nuovo_vocabolo()
# st.header("Nuovo vocabolo")

# with st.form("nuovo_vocabolo"):
#     t: Transcription = Transcription(
#     )
#     st.subheader("Italiano")
#     vocabolo_ita = st.text_input('Italiano', placeholder='Inserisci il vocabolo in italiano')
#     st.subheader("Bivongese")
#     vocabolo_tradotto = st.text_input('Tradotto', placeholder='Inserisci il vocabolo tradotto')

#     st.subheader("Audio")
#     upload_dd_col, record_col = st.columns(2)

#     audio_path = None
#     with upload_dd_col:
#         st.text("Carica file audio")
#         uploaded_file = st.file_uploader("Carica un file audio",type=ALLOWED_AUDIO_EXT)
#         if uploaded_file is not None:
#             st.session_state.is_mic_recording = False
#             st.audio(data=uploaded_file.getvalue(), format=f"audio/{str(uploaded_file.name).split('.')[-1]}")

#     with record_col:
#         st.text("Registra da microfono")
#         wav_audio_data = st_audiorec()

#         if wav_audio_data is not None:
#             st.session_state.is_mic_recording = True

#     # Every form must have a submit button.
#     submitted = st.form_submit_button("Aggiungi")
#     if submitted:
#         good=True
#         # Check ita
#         if vocabolo_ita is not None and str(vocabolo_ita).strip() != "":
#             t.update(it_term=str(vocabolo_ita))
#         else:
#             good=False
#         # Check biv
#         if vocabolo_tradotto is not None and str(vocabolo_tradotto).strip() != "":
#             t.update(biv_term=str(vocabolo_tradotto))
#         else:
#             good=False
#         # Check audio
#         if st.session_state.is_mic_recording and wav_audio_data is not None:
#                 audio_path: Path = salvaRegistrazioneAudio(audio_data=wav_audio_data)
#                 t.update(audio_path=audio_path)
#         elif not st.session_state.is_mic_recording and uploaded_file is not None:
#                 audio_path: Path = salvaFileAudio(uploaded_file=uploaded_file)
#                 t.update(audio_path=audio_path)
#         else:
#             good=False
        
#         # check finale
#         if good:
#             print("dump vocabolo prima insert")
#             print(str(t.model_dump_json()))
#             creaVocabolo(vocabolo=t)
#             st.success("Aggiunto")
#         else:
#             st.error("Non aggiunto")