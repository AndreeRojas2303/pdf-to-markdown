"""
pdf_a_md.py — Convierte PDFs a Markdown por lotes.

Instalación (una sola vez):
    pip install pymupdf4llm

Uso:
    python pdf_a_md.py                      # convierte todos los PDF de la carpeta actual
    python pdf_a_md.py C:\\ruta\\a\\pdfs     # convierte todos los PDF de esa carpeta
    python pdf_a_md.py archivo.pdf          # convierte un solo archivo
    python pdf_a_md.py --imagenes           # además extrae las figuras a /media

Salida: un .md por cada PDF, en una subcarpeta "markdown".
Las imágenes usan nombres cortos (p01-0001-02.png) para no exceder
el límite de 260 caracteres de rutas de Windows.
"""

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

try:
    import pymupdf4llm
    import pymupdf
except ImportError:
    sys.exit("Falta la librería. Ejecuta:  pip install pymupdf4llm")


UMBRAL_TEXTO = 100  # caracteres mínimos por página para asumir que hay capa de texto


def tiene_capa_de_texto(pdf: Path) -> bool:
    """Detecta si el PDF es escaneado (imagen pura) revisando las primeras páginas."""
    doc = pymupdf.open(pdf)
    paginas = min(5, doc.page_count)
    total = sum(len(doc[i].get_text().strip()) for i in range(paginas))
    doc.close()
    return total > UMBRAL_TEXTO * paginas / 2


def convertir(pdf: Path, salida_dir: Path, extraer_imagenes: bool, indice: int) -> bool:
    destino = salida_dir / f"{pdf.stem}.md"

    if not tiene_capa_de_texto(pdf):
        print(f"  [OMITIDO] {pdf.name} parece escaneado (sin capa de texto). Necesita OCR.")
        return False

    if not extraer_imagenes:
        texto = pymupdf4llm.to_markdown(str(pdf))
        destino.write_text(texto, encoding="utf-8")
        print(f"  [OK] {pdf.name} -> {destino.name} ({destino.stat().st_size / 1024:.0f} KB)")
        return True

    # Con imágenes: se trabaja sobre una copia de nombre corto para no
    # reventar el límite de rutas de Windows, y luego se corrigen los enlaces.
    corto = f"p{indice:02d}"
    media = salida_dir / "media"
    media.mkdir(parents=True, exist_ok=True)

    temporal = Path(tempfile.mkdtemp(prefix="pdfmd_"))
    try:
        copia = temporal / f"{corto}.pdf"
        shutil.copy2(pdf, copia)

        texto = pymupdf4llm.to_markdown(
            str(copia),
            write_images=True,
            image_path=str(media),
            image_format="png",
            dpi=200,
        )
    finally:
        shutil.rmtree(temporal, ignore_errors=True)

    # Reescribe las rutas absolutas de las imágenes a rutas relativas: media/...
    texto = texto.replace(str(media) + "\\", "media/")
    texto = texto.replace(str(media) + "/", "media/")

    destino.write_text(texto, encoding="utf-8")
    n_img = len(list(media.glob(f"{corto}-*.png")))
    print(f"  [OK] {pdf.name} -> {destino.name} "
          f"({destino.stat().st_size / 1024:.0f} KB, {n_img} imagenes como {corto}-*)")
    return True


def main():
    ap = argparse.ArgumentParser(description="Convierte PDFs a Markdown por lotes.")
    ap.add_argument("ruta", nargs="?", default=".", help="Archivo PDF o carpeta con PDFs")
    ap.add_argument("--imagenes", action="store_true", help="Extraer figuras a /media")
    ap.add_argument("--salida", default=None, help="Carpeta de salida (por defecto ./markdown)")
    args = ap.parse_args()

    ruta = Path(args.ruta).expanduser().resolve()
    if not ruta.exists():
        sys.exit(f"No existe la ruta: {ruta}")

    if ruta.is_file():
        pdfs = [ruta]
        base = ruta.parent
    else:
        pdfs = sorted(ruta.glob("*.pdf"))
        base = ruta

    if not pdfs:
        sys.exit(f"No se encontraron PDFs en {base}")

    salida_dir = Path(args.salida).resolve() if args.salida else base / "markdown"
    salida_dir.mkdir(parents=True, exist_ok=True)

    print(f"Convirtiendo {len(pdfs)} archivo(s) -> {salida_dir}\n")

    exitosos, fallidos, omitidos = 0, [], 0
    for i, pdf in enumerate(pdfs, start=1):
        try:
            if convertir(pdf, salida_dir, args.imagenes, i):
                exitosos += 1
            else:
                omitidos += 1
        except Exception as e:
            print(f"  [ERROR] {pdf.name}: {e}")
            fallidos.append(pdf.name)

    print(f"\nListo. {exitosos} convertidos, {omitidos} omitidos, {len(fallidos)} con error.")
    if fallidos:
        print("Con error:", ", ".join(fallidos))


if __name__ == "__main__":
    main()
