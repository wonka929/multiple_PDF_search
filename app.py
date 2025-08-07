import streamlit as st
import fitz  # PyMuPDF
import os
import re
from urllib.parse import quote
import uuid

PDF_DIR = "pdfs"
PDF_SERVER_URL = "http://localhost:8000"  # Web server esterno

# Estrae testo da tutti i PDF
@st.cache_data(show_spinner=False)
def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    results = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        # Salva l'intera pagina come un unico record
        results.append({
            "file": os.path.basename(pdf_path),
            "page": page_num,
            "text": text.strip(),
            "path": pdf_path
        })
    return results

# Interfaccia Streamlit
st.set_page_config(page_title="Ricerca PDF", page_icon="🔍")
st.title("🔍 Ricerca nei PDF")

query = st.text_input("Inserisci una parola o frase da cercare:")

# Selezione file PDF (opzionale)
available_files = sorted([f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")])
selected_files = st.multiselect("Filtra per file PDF:", available_files, default=available_files)

if not os.path.exists(PDF_DIR):
    st.error(f"La cartella '{PDF_DIR}' non esiste. Creala e inserisci i tuoi PDF.")
else:
    all_results = []
    pdf_files = selected_files
    #pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]

    with st.spinner("Estrazione testo dai PDF..."):
        for pdf_file in pdf_files:
            path = os.path.join(PDF_DIR, pdf_file)
            all_results.extend(extract_pdf_text(path))

    if query:
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        matches = [res for res in all_results if pattern.search(res["text"])]

        # Evita duplicati esatti
        seen = set()
        unique_matches = []
        for match in matches:
            key = (match["file"], match["page"], match["text"])
            if key not in seen:
                seen.add(key)
                unique_matches.append(match)

        st.success(f"Trovate {len(unique_matches)} occorrenze.")

        for match in unique_matches:
            st.markdown(f"**File:** `{match['file']}` — **Pagina:** {match['page']}")
            # Mostra una porzione di testo più lunga (es: 400 caratteri centrati sul match)
            text = match['text']
            query_match = pattern.search(text)
            if query_match:
                match_start = query_match.start()
                match_end = query_match.end()
                window = 400
                center = (match_start + match_end) // 2
                start = max(center - window // 2, 0)
                end = min(center + window // 2, len(text))
                excerpt = text[start:end]
                excerpt = excerpt.replace('\n', ' ')
                # Evidenzia la query nell'estratto con sfondo giallo (HTML)
                def highlight_html(text, pattern):
                    return re.sub(pattern, lambda m: f'<span style="background-color:yellow;font-weight:bold;">{m.group(0)}</span>', text)
                highlighted_html = highlight_html(excerpt, pattern)
                st.markdown(f"... {highlighted_html.strip()} ...", unsafe_allow_html=True)
            else:
                st.write(text)

            # Link per aprire il PDF alla pagina corretta nel browser
            pdf_url = f"{PDF_SERVER_URL}/{quote(match['file'])}#page={match['page']}"

            st.markdown(
                f"[📂 Apri a pagina {match['page']}]({pdf_url})",
                unsafe_allow_html=True
            )

            st.markdown("---")
