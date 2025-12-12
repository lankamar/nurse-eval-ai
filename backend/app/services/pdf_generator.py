import hashlib
import json
from pathlib import Path
from typing import Dict

import qrcode
from fpdf import FPDF


def _build_qr(data: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    qr_path = output_dir / "qr.png"
    img = qrcode.make(data)
    img.save(qr_path)
    return qr_path


def generate_pdf(
    evaluation_id: int,
    scores: Dict[str, int],
    total_score: str,
    classification: str,
    output_dir: Path,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / f"evaluation_{evaluation_id}.pdf"

    payload = json.dumps({"evaluation_id": evaluation_id, "scores": scores, "total": total_score}, sort_keys=True)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    qr_path = _build_qr(digest, output_dir)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "NurseEval AI - Evaluación Oficial", ln=True)
    pdf.cell(0, 10, f"ID Evaluación: {evaluation_id}", ln=True)
    pdf.cell(0, 10, f"Total: {total_score} | Clasificación: {classification}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, "Scores:", ln=True)
    for k, v in scores.items():
        pdf.cell(0, 8, f"  {k}: {v}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, f"Hash SHA-256: {digest}", ln=True)
    pdf.image(str(qr_path), w=30)
    pdf.output(str(pdf_path))
    return pdf_path
