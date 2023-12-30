### Come avviare l'applicazione

- andare su Start e digitare powershell
- cliccare semplicemente su "Windows Powershell"
- Una volta che un terminale nero si è aperto copiare il seguente comando

```powershell
cd $env:USERPROFILE"\Documents\app dizionario\dizionario-papa"
```
- Ora il terminale dovrebbe indicare che si trova nella cartella "dizionario-papa"
- Copiare ed incollare nel terminale il seguente comando per avviare l'applicazione
```powershell
Set-ExecutionPolicy Unrestricted -Scope Process;..\Scripts\Activate.ps1;streamlit run .\home.py
```

- dovrebbe avviarsi la applicazione e aprire in autonomia Google Chrome

### Chiudere l'applicazione
- **per chiudere** la applicazione correttamente:
    - chiudere la tab su google chrome
    - **selezionando il terminale precedentemente usato schiacciare CTRL-C** oppure **Chiudere la finestra del terminale**
