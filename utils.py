import logging
from pathlib import Path
import traceback
from typing import List

import streamlit as st
from st_audiorec import st_audiorec

from model import Transcription, create_transcription, search_transcriptions, update_transcription

DATA_DIR : Path = Path(Path(__file__).parent,"data")
BACKUP_DIR : Path = Path(Path(__file__).parent,"backup")
DATA_AUDIO_DIR : Path = Path(DATA_DIR,"audio")

def check_folder_existance():
    # Check folders exists
    check_folders = [DATA_DIR,BACKUP_DIR,DATA_AUDIO_DIR]
    for folder in check_folders:
        if not folder.is_dir() or not folder.exists():
            folder.mkdir(parents=True,exist_ok=True)
    
ALLOWED_AUDIO_EXT = ["wav","mp3"]

def salvaFileAudio(uploaded_file):
    file_name = str(uploaded_file.name)
    return salvaAudio(data=uploaded_file.getvalue(),name=file_name)
    
def salvaRegistrazioneAudio(audio_data):
    from datetime import datetime
    file_name = f"mic_{datetime.now().strftime('%Y%m%d%H%M%S')}.wav"
    return salvaAudio(data=audio_data,name=file_name)

def salvaAudio(data,name):
    audio_path_dst: Path = Path(DATA_AUDIO_DIR,name) 
    try:
        with open(audio_path_dst, 'wb') as f: 
            f.write(data)
            st.success('File audio salvato')
            return audio_path_dst
    except Exception as e:
        logging.error('Errore - File audio non salvato')
        traceback.print_exc()
        logging.error(e)
        raise ValueError("Salvataggio file audio fallito")

# audio_path_dst: Path = salvaFileAudio(uploaded_file=uploaded_file)
# # Salvato l'audio nella cartella

def creaVocabolo(vocabolo):
    try:
        # preparare oggetto per poi salvarlo nel db
        created = create_transcription(transcription=vocabolo)
        logging.debug(f"created transcription {created.model_dump_json()}")
        st.success('Vocabolo salvato')
    except Exception as e:
        traceback.print_exc()
        logging.error(e)
        st.error('Errore - Vocabolo non salvato')

def aggiornaVocabolo(vocabolo):
    try:
        # preparare oggetto per poi salvarlo nel db
        created = update_transcription(transcription=vocabolo)
        logging.debug(f"created transcription {created.model_dump_json()}")
        st.success('Vocabolo salvato')
    except Exception as e:
        traceback.print_exc()
        logging.error(e)
        st.error('Errore - Vocabolo non salvato')


def form_nuovo_vocabolo():
    st.header("Nuovo vocabolo")
    with st.form("nuovo_vocabolo"):
        t: Transcription = Transcription(
        )
        st.subheader("Italiano")
        vocabolo_ita = st.text_input('Italiano', placeholder='Inserisci il vocabolo in italiano')
        st.subheader("Bivongese")
        vocabolo_tradotto = st.text_input('Tradotto', placeholder='Inserisci il vocabolo tradotto')

        st.subheader("Audio")
        upload_dd_col, record_col = st.columns(2)

        audio_path = None
        with upload_dd_col:
            st.text("Carica file audio")
            uploaded_file = st.file_uploader("Carica un file audio",type=ALLOWED_AUDIO_EXT)
            if uploaded_file is not None:
                st.session_state.is_mic_recording = False
                st.audio(data=uploaded_file.getvalue(), format=f"audio/{str(uploaded_file.name).split('.')[-1]}")

        with record_col:
            st.text("Registra da microfono")
            wav_audio_data = st_audiorec()

            if wav_audio_data is not None:
                st.session_state.is_mic_recording = True

        # Every form must have a submit button.
        submitted = st.form_submit_button("Aggiungi")
        if submitted:
            good=True
            # Check ita
            if vocabolo_ita is not None and str(vocabolo_ita).strip() != "":
                t.update(it_term=str(vocabolo_ita))
            else:
                good=False
            # Check biv
            if vocabolo_tradotto is not None and str(vocabolo_tradotto).strip() != "":
                t.update(biv_term=str(vocabolo_tradotto))
            else:
                good=False
            # Check audio
            if st.session_state.is_mic_recording and wav_audio_data is not None:
                    audio_path: Path = salvaRegistrazioneAudio(audio_data=wav_audio_data)
                    t.update(audio_path=audio_path)
            elif not st.session_state.is_mic_recording and uploaded_file is not None:
                    audio_path: Path = salvaFileAudio(uploaded_file=uploaded_file)
                    t.update(audio_path=audio_path)
            else:
                good=False
            
            # check finale
            if good:
                print("dump vocabolo prima insert")
                print(str(t.model_dump_json()))
                creaVocabolo(vocabolo=t)
                st.success("Aggiunto")
            else:
                st.error("Non aggiunto")


def form_aggiorna_vocabolo(vocabolo: Transcription):
    with st.form("aggiorna_vocabolo"):
        t: Transcription = vocabolo
        st.subheader("Italiano")
        vocabolo_ita = st.text_input('Italiano', placeholder='Inserisci il vocabolo in italiano',value=t.it_term)
        st.subheader("Bivongese")
        vocabolo_tradotto = st.text_input('Tradotto', placeholder='Inserisci il vocabolo tradotto',value=t.biv_term)

        st.subheader("Audio")
        # load old audio
        # str(Path(str(t.audio_path)))
        
        st.audio(data=str(t.audio_path), format=f"audio/{str(t.audio_path).split('.')[-1]}")
        upload_dd_col, record_col = st.columns(2)

        audio_path = None
        with upload_dd_col:
            st.text("Carica file audio")
            uploaded_file = st.file_uploader("Carica un file audio",type=ALLOWED_AUDIO_EXT,label_visibility='hidden')
            if uploaded_file is not None:
                st.session_state.is_mic_recording = False
                st.audio(data=uploaded_file.getvalue(), format=f"audio/{str(uploaded_file.name).split('.')[-1]}")

        with record_col:
            st.text("Registra da microfono")
            wav_audio_data = st_audiorec()

            if wav_audio_data is not None:
                st.session_state.is_mic_recording = True

        # Every form must have a submit button.
        submitted = st.form_submit_button("Aggiungi")
        if submitted:
            good=True
            # Check ita
            if vocabolo_ita is not None and str(vocabolo_ita).strip() != "":
                t.update(it_term=str(vocabolo_ita))
            else:
                good=False
            # Check biv
            if vocabolo_tradotto is not None and str(vocabolo_tradotto).strip() != "":
                t.update(biv_term=str(vocabolo_tradotto))
            else:
                good=False
            # Check audio
            if st.session_state.is_mic_recording and wav_audio_data is not None:
                    audio_path: Path = salvaRegistrazioneAudio(audio_data=wav_audio_data)
                    t.update(audio_path=audio_path)
            elif not st.session_state.is_mic_recording and uploaded_file is not None:
                    audio_path: Path = salvaFileAudio(uploaded_file=uploaded_file)
                    t.update(audio_path=audio_path)
            else:
                good=False
            
            # check finale
            if good:
                print("dump vocabolo prima insert")
                print(str(t.model_dump_json()))
                aggiornaVocabolo(vocabolo=t)
                st.success("Aggiornato")
            else:
                st.error("Non aggiornato")

def search_vocabolario(searchterm: str) -> List[any]:
    transcription_list = search_transcriptions(searchterm)
    return transcription_list

def filter_vocab_data(vl: List[Transcription]):
    tmp_set = set(vl)
    return list(tmp_set)

def filtered_search_vocabolario(searchterm: str) -> List[any]:
    transcription_list = search_transcriptions(searchterm)
    return filter_vocab_data(transcription_list)