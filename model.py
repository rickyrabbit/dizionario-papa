import logging
import traceback
from uuid import uuid4
from pathlib import Path

import sqlite3
# from fastapi import FastAPI, HTTPException, Query, Path, File
from pydantic import BaseModel, Field, validator
from dbutils import db_path
# app = FastAPI()

# Initialize the SQLite database connection

# Create a table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS transcriptions (
    id TEXT PRIMARY KEY,
    it_term TEXT NOT NULL,
    biv_term TEXT NOT NULL,
    audio_path TEXT NOT NULL
)
"""
# conn = sqlite3.connect(str(db_path), check_same_thread=False)
def init_dbconn():
    # check file exists, if not create empty one
    if not db_path.exists() or not db_path.is_file():
        db_path.touch(exist_ok=True)
    dbconn = sqlite3.connect(str(db_path), check_same_thread=False)
    try:
        dbconn.execute(create_table_query)
    finally:
        dbconn.close()
       
init_dbconn()


class Transcription(BaseModel):
    """
    A Pydantic model representing a transcription entry.

    Attributes:
        id: A unique identifier for the transcription entry, generated using
            uuid4.
        it_term: A string representation of the Italian term.
        biv_term: A string representation of the English term.
        audio_path: A Path object pointing to the corresponding audio file.
    """

    id: str = Field(default_factory=lambda: uuid4().hex, repr=False)  # Generate a unique ID using uuid4
    it_term: str = Field(default="", repr=True)  # Italian term
    biv_term: str = Field(default="", repr=True)  # English term
    audio_path: Path = Field(default=None, repr=False) # Audio file Path object

    @validator('audio_path')
    def audio_path_validator(cls, v):
        if isinstance(v,Path):
            return v
        elif isinstance(v,str):
            return Path(v)
        elif v is None:
            return None
        else:
            logging.debug("path not handled properly")
            return None
        

    def __key(self):
        return (self.id, self.it_term, self.biv_term)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Transcription):
            return self.__key() == other.__key()
        return NotImplemented
    
    def update(
        self,
        it_term: str = None,
        biv_term: str = None,
        audio_path: Path = None
    ):
        if it_term is not None:
            self.it_term = it_term
        if biv_term is not None:
            self.biv_term = biv_term
        if audio_path is not None:
            self.audio_path = audio_path


# conn.execute(create_table_query)

# Read all transcriptions
# @app.get('/transcriptions')
def get_transcriptions():
    transcriptions = []
    try:
        db = sqlite3.connect(str(db_path), check_same_thread=False)
        c = db.cursor()
        try:
            # for row in c.execute('SELECT id,it_term,biv_term,audio_path FROM transcriptions'):
            transcription_keys = list(Transcription.model_json_schema().get("properties").keys())
            for row in c.execute('SELECT * FROM transcriptions'):
                # print(row)
                # print(Transcription.model_json_schema().get("properties").keys())
                row_values = [*row] # row values
                d = dict(zip(transcription_keys,row_values))
                transcriptions.append(Transcription(**d))
        except Exception as e:
            logging.error(e)
            traceback.print_exc()
        finally:
            c.close()
    finally:
        db.close() 
    return transcriptions

def search_transcriptions(pattern:str):
    transcriptions = []
    try:
        db = sqlite3.connect(str(db_path), check_same_thread=False)
        c = db.cursor()
        try:
            # for row in c.execute('SELECT id,it_term,biv_term,audio_path FROM transcriptions'):
            transcription_keys = list(Transcription.model_json_schema().get("properties").keys())
            search_pattern_sql = f"""
            SELECT *
            FROM transcriptions AS t
            WHERE LOWER(t.it_term) LIKE '%{str(pattern)}%' OR LOWER(t.biv_term) LIKE '%{str(pattern)}%'
            """
            for row in c.execute(search_pattern_sql):
                # print(row)
                # print(Transcription.model_json_schema().get("properties").keys())
                row_values = [*row] # row values
                d = dict(zip(transcription_keys,row_values))
                transcriptions.append(Transcription(**d))
        except Exception as e:
            logging.error(e)
            traceback.print_exc()
        finally:
            c.close()
    finally:
        db.close() 
    return transcriptions

# Create a new transcription
# @app.post('/transcriptions')
def create_transcription(transcription: Transcription):
    # Check if the audio file exists
    # print(transcription)
    if not transcription.audio_path.is_file():
        raise Exception(dict(status_code=400, detail='Audio file doesn\'t exist'))

    # Insert the transcription into the database
    insert_query = """
    INSERT INTO transcriptions (
        id, it_term, biv_term, audio_path
    ) VALUES (?, ?, ?, ?)
    """
    try:
        db = sqlite3.connect(str(db_path), check_same_thread=False)
        c = db.cursor()
        try:
            t_dump = transcription.model_dump()
            c.execute(insert_query, (str(t_dump.get("id")), str(t_dump.get("it_term")),
                                    str(t_dump.get("biv_term")), str(t_dump.get("audio_path"))))
            db.commit()
        except Exception as e:
            logging.error(e)
            traceback.print_exc()
        finally:
            c.close()
    except Exception as e:
            logging.error(e)
            traceback.print_exc()
    finally:
        db.close() 

    return transcription

# Retrieve a specific transcription by ID
# @app.get('/transcriptions/{id}')
def get_transcription_by_id(transcription: Transcription):
    try:
        db = sqlite3.connect(str(db_path), check_same_thread=False)
        c = db.cursor()
        try:
            transcription = c.execute('SELECT * FROM transcriptions WHERE id=?', (str(transcription.id),)).fetchone()
        except Exception as e:
            logging.error(e)
            traceback.print_exc()
    except Exception as e:
            logging.error(e)
            traceback.print_exc()
    finally:
        db.close() 
        # Check if the transcription exists
        if transcription is None:
            raise Exception(dict(status_code=404, detail='Transcription not found'))

        return Transcription(**transcription)


# Update an existing transcription
# @app.put('/transcriptions/{id}')
def update_transcription(transcription: Transcription):
    # Check if the transcription exists
    try:
        db = sqlite3.connect(str(db_path), check_same_thread=False)
        c = db.cursor()
        try:
            _res = c.execute('SELECT * FROM transcriptions WHERE id=?', (str(transcription.id),)).fetchone()
            if _res is not None:
                transcription_exists = True
            else:
                transcription_exists = False
                raise ValueError(f"No transcriptions with id {str(transcription.id)}")
        except Exception as e:
            logging.error(e)
            traceback.print_exc()
        finally:
            c.close()

        c = db.cursor() 
        try:
            if not transcription_exists:
                raise Exception(dict(status_code=404, detail='Transcription not found'))
            
            # Check if the audio file exists (update requires existing file)
            if not transcription.audio_path.is_file():
                raise Exception(dict(status_code=404, detail='Audio file doesn\'t exist'))

            # Update the transcription in the database
            update_query = """
            UPDATE transcriptions SET it_term=?, biv_term=?, audio_path=? WHERE id=?
            """
            c.execute(update_query, (transcription.it_term, transcription.biv_term,
                                    str(transcription.audio_path.absolute()), str(transcription.id)))
            db.commit()
        except Exception as e:
            logging.error(e)
            traceback.print_exc()
    except Exception as e:
            logging.error(e)
            traceback.print_exc()
    finally:
        db.close()

    return transcription

# @app.delete('/transcriptions/{id}')
def delete_transcription(transcription: Transcription):
    # Check if the transcription exists
    try:
        db = sqlite3.connect(str(db_path), check_same_thread=False)
        c = db.cursor()
        try:
            transcription = c.execute('SELECT * FROM transcriptions WHERE id=?', (str(transcription.id),)).fetchone()
            transcription_exists = transcription is not None
        except Exception as e:
            logging.error(e)
            traceback.print_exc()
        finally:
            c.close()

        c = db.cursor() 
        try:
            if not transcription_exists:
                raise Exception(dict(status_code=404, detail='Transcription not found'))
            
            # Check if the audio file exists (update requires existing file)
            if not transcription.audio_path.is_file():
                raise Exception(dict(status_code=404, detail='Audio file doesn\'t exist'))

            # Delete the transcription from the database
            delete_query = """
            DELETE FROM transcriptions WHERE id=?
            """
            c.execute(delete_query, (str(transcription.id),))

            # Delete the associated audio file
            audio_path = transcription.audio_path
            audio_path.unlink()
            print('Transcription deleted successfully')
        except Exception as e:
            logging.error(e)
            traceback.print_exc()
    except Exception as e:
            logging.error(e)
            traceback.print_exc()
    finally:
        db.close()





