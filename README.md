# PDF to Markdown (batch converter)

A small Python script that converts **multiple PDF files to Markdown at once**, entirely on your own computer. Optionally, it also extracts the images inside each PDF.

I built it (with the help of Claude) to prepare academic papers for AI-assisted work: literature reviews, summaries, and presentation slides. Because it runs locally, your documents are never uploaded anywhere.

## Features

- Converts every PDF in a folder in a single run
- Saves the results in a new `markdown` folder
- Optional image extraction with `--imagenes`
- Skips files that are not PDFs
- Prints a final summary: converted, skipped, and failed files

## Requirements

- Python 3
- [pymupdf4llm](https://pypi.org/project/pymupdf4llm/)

```bash
pip install -r requirements.txt
```

## Usage

1. Download `pdf_a_md.py` and place it in the same folder as your PDF files.
2. Open a terminal (PowerShell on Windows) and go to that folder. Tip: you can copy the folder path from the address bar of your file explorer.

   ```bash
   cd "C:\path\to\your\folder"
   ```

3. Run the script:

   ```bash
   python pdf_a_md.py
   ```

   To also extract images:

   ```bash
   python pdf_a_md.py --imagenes
   ```

4. Your converted files will be in the new `markdown` folder.

Example output:

```
Convirtiendo 1 archivo(s) -> ...\markdown

  [OK] paper.pdf -> paper.md (59 KB, 0 imagenes como p01-*)

Listo. 1 convertidos, 0 omitidos, 0 con error.
```

## Limitations

- Only PDF files are supported (Word documents are skipped).
- Image extraction is not always precise: it may also extract logos and decorative elements, so review the images before using them.
- Scanned PDFs (images of text) may not convert well, since the script does not run OCR.

## How I use it

This script is the first step of my workflow for turning research papers into presentations:

1. Convert papers to Markdown and extract their figures with this script.
2. Use Claude to draft a slide-building guide from the Markdown files and numbered figures.
3. Review and edit the guide myself.
4. Run it with Claude Code and PPT Master to produce fully editable slides, with the original figures inserted and cited.

---

### En español

Script en Python que convierte varios PDF a Markdown de una sola vez, de forma local. Coloca `pdf_a_md.py` en la carpeta de tus PDF, abre PowerShell, entra a la carpeta con `cd` y ejecuta `python pdf_a_md.py`. Añade `--imagenes` al final si también quieres extraer las imágenes. Los archivos convertidos aparecerán en la carpeta `markdown`.
