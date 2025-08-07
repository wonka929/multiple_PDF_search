#!/bin/bash

# Vai nella cartella dello script
cd "$(dirname "$0")"

# Controlla se la cartella pdfs esiste
if [ ! -d "pdfs" ]; then
  echo "❌ Errore: la cartella 'pdfs/' non esiste."
  exit 1
fi

# Avvia il web server locale per i PDF sulla porta 8000
echo "📂 Avvio web server per PDF sulla porta 8000..."
(cd pdfs && python3 -m http.server 8000) &
PDF_SERVER_PID=$!

# Aspetta un po’ che si avvii
sleep 1

# Avvia Streamlit
echo "🚀 Avvio Streamlit..."
streamlit run app.py

# Quando Streamlit si chiude, termina anche il web server
echo "🛑 Chiudo il web server..."
kill $PDF_SERVER_PID

