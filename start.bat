@echo off
REM Vai nella cartella dello script
cd /d %~dp0

REM Controlla se la cartella pdfs esiste
if not exist "pdfs" (
    echo Errore: la cartella 'pdfs' non esiste.
    exit /b 1
)

REM Avvia il web server locale per i PDF sulla porta 8000
echo Avvio web server per PDF sulla porta 8000...
start "PDFServer" cmd /c "cd pdfs && python -m http.server 8000"
REM Attendi un secondo per l'avvio
ping -n 2 127.0.0.1 >nul

REM Avvia Streamlit
echo Avvio Streamlit...
streamlit run app.py

REM Chiudi il web server (trova il processo e termina)
echo Chiudo il web server...
taskkill /f /im python.exe >nul 2>&1
