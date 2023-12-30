# Guida installazione
### Creazione cartella
Crea cartella nei Documenti, chiamandola **app dizionario**
### 


## Dipendenze del progetto

[x] Creato un requirements.txt

### Setup venv
Messi allo stesso livello della cartella da cui è stato fatto il clone della repo
```powershell
python -m venv .
```
Il venv creato dovrebbe chiamarsi di default come la cartella in cui si era nel terminale


### Attivazione venv
```powershell
Set-ExecutionPolicy Unrestricted -Scope Process;..\Scripts\Activate.ps1
```

### Installazione requisiti progetto
```powershell
(venv) pip install -r requirements.txt
```

### Avvia app
```powershell
(venv) streamlit run .\home.py
```

