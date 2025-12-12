from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import hashlib
import os
from sqlalchemy.orm import Session

from app.models.models import Evaluation, EvaluationResponse, Criteria


class PDFService:
    """Generate auditable PDF reports for evaluations (Ley 25.326 compliance)."""
    
    def __init__(self, output_dir: str = "generated_pdfs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_evaluation_pdf(self, evaluation_id: int, db: Session) -> dict:
        """Generate PDF report for evaluation."""
        evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
        if not evaluation:
            return None
        
        # Generate filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"evaluation_{evaluation_id}_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=12
        )
        
        # Title
        story.append(Paragraph("EVALUACIÓN DE DESEMPEÑO - ENFERMERÍA", title_style))
        story.append(Paragraph("Hospital de Clínicas José de San Martín - UBA", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Regulatory compliance header
        story.append(Paragraph("Marco Normativo:", heading_style))
        compliance_text = """
        Esta evaluación se realiza conforme a:<br/>
        • Decreto 366/06 - Evaluación de Desempeño del Personal de Enfermería<br/>
        • Ley 25.326 - Protección de Datos Personales<br/>
        • RENFAMED - Registro Nacional de Profesionales de Salud
        """
        story.append(Paragraph(compliance_text, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Evaluation metadata
        story.append(Paragraph("Información General:", heading_style))
        metadata = [
            ['ID Evaluación:', str(evaluation.id)],
            ['Período:', evaluation.period],
            ['Evaluador:', f"{evaluation.evaluator.full_name} ({evaluation.evaluator.role.value})"],
            ['Evaluado:', f"{evaluation.evaluated.full_name} ({evaluation.evaluated.role.value})"],
            ['Fecha Creación:', evaluation.created_at.strftime("%d/%m/%Y %H:%M")],
            ['Estado:', evaluation.status.value],
            ['Consentimiento:', 'Sí' if evaluation.consent_given else 'No'],
        ]
        
        if evaluation.completed_at:
            metadata.append(['Fecha Finalización:', evaluation.completed_at.strftime("%d/%m/%Y %H:%M")])
        
        metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e6f2ff')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(metadata_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Scores summary
        story.append(Paragraph("Resumen de Calificaciones:", heading_style))
        scores_data = [
            ['Competencia', 'Puntaje'],
            ['Técnicas', f"{evaluation.technical_score or 0:.2f}%"],
            ['Actitudinales', f"{evaluation.attitudinal_score or 0:.2f}%"],
            ['TOTAL', f"{evaluation.total_score or 0:.2f}%"],
        ]
        
        scores_table = Table(scores_data, colWidths=[3*inch, 2*inch])
        scores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e6f2ff')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        story.append(scores_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Detailed responses
        story.append(PageBreak())
        story.append(Paragraph("Evaluación Detallada por Competencias:", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        responses = db.query(EvaluationResponse).filter(
            EvaluationResponse.evaluation_id == evaluation_id
        ).all()
        
        # Group by criteria type
        technical_responses = []
        attitudinal_responses = []
        
        for response in responses:
            criteria = db.query(Criteria).filter(Criteria.id == response.criteria_id).first()
            if criteria:
                response_data = [
                    criteria.code,
                    criteria.name,
                    f"{response.score}/{criteria.max_score}",
                    response.comments or "-"
                ]
                
                if criteria.criteria_type.value == "tecnica":
                    technical_responses.append(response_data)
                else:
                    attitudinal_responses.append(response_data)
        
        # Technical competencies
        if technical_responses:
            story.append(Paragraph("A. Competencias Técnicas (11 criterios):", heading_style))
            tech_data = [['Código', 'Competencia', 'Puntaje', 'Comentarios']] + technical_responses
            tech_table = Table(tech_data, colWidths=[0.7*inch, 2.5*inch, 0.8*inch, 2*inch])
            tech_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (2, 0), (2, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(tech_table)
            story.append(Spacer(1, 0.2*inch))
        
        # Attitudinal competencies
        if attitudinal_responses:
            story.append(Paragraph("B. Competencias Actitudinales (14 criterios):", heading_style))
            att_data = [['Código', 'Competencia', 'Puntaje', 'Comentarios']] + attitudinal_responses
            att_table = Table(att_data, colWidths=[0.7*inch, 2.5*inch, 0.8*inch, 2*inch])
            att_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (2, 0), (2, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(att_table)
            story.append(Spacer(1, 0.2*inch))
        
        # General comments
        if evaluation.comments:
            story.append(Paragraph("Observaciones Generales:", heading_style))
            story.append(Paragraph(evaluation.comments, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Footer with audit information
        story.append(PageBreak())
        story.append(Paragraph("Información de Auditoría:", heading_style))
        audit_info = f"""
        Documento generado el {datetime.utcnow().strftime("%d/%m/%Y a las %H:%M:%S UTC")}.<br/>
        Este documento es auditable y cumple con los requisitos de Ley 25.326 de Protección de Datos Personales.<br/>
        Cualquier modificación del contenido invalidará el hash de verificación.
        """
        story.append(Paragraph(audit_info, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        # Calculate hash for audit trail
        pdf_hash = self._calculate_file_hash(filepath)
        
        # Update evaluation record
        evaluation.pdf_generated = True
        evaluation.pdf_path = filepath
        evaluation.pdf_hash = pdf_hash
        db.commit()
        
        return {
            "pdf_path": filepath,
            "pdf_hash": pdf_hash,
            "filename": filename
        }
    
    def _calculate_file_hash(self, filepath: str) -> str:
        """Calculate SHA-256 hash of file for audit trail."""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
