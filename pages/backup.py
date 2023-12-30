from datetime import datetime
import os
from pathlib import Path
import time
import streamlit as st

import shutil

st.header("Backup dizionario")
gd_auth = st.button("Esegui Backup", type="primary")

DATA_DIR : Path = Path(Path(__file__).parent.parent,"data")
BACKUP_DIR : Path = Path(Path(__file__).parent.parent,"backup")

if gd_auth:
    my_bar = st.progress(0, text="")
    for percent_complete in range(50):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text="Backup in corso")
    zip_file_dst : Path = Path(BACKUP_DIR,f"backup_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    saved_file_name = shutil.make_archive(str(zip_file_dst), 'zip', DATA_DIR)
    if saved_file_name:
        my_bar.progress(100, text="Backup completato")



