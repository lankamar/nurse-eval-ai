"""
Seed data for evaluation criteria based on Decreto 366/06
11 Technical (Técnicas) + 14 Attitudinal (Actitudinales) criteria
"""

from sqlalchemy.orm import Session
from app.models.models import Criteria, CriteriaType, User, RoleEnum
from app.core.security import get_password_hash


def seed_criteria(db: Session):
    """Seed evaluation criteria per Decreto 366/06."""
    
    # Check if criteria already exist
    existing_criteria = db.query(Criteria).first()
    if existing_criteria:
        print("Criteria already seeded")
        return
    
    # 11 Technical Criteria (Competencias Técnicas)
    technical_criteria = [
        {
            "code": "TEC-01",
            "name": "Conocimientos Técnicos Específicos",
            "description": "Dominio de técnicas y procedimientos específicos de enfermería según área de desempeño",
            "order": 1
        },
        {
            "code": "TEC-02",
            "name": "Aplicación de Normas de Bioseguridad",
            "description": "Cumplimiento riguroso de protocolos de bioseguridad e higiene hospitalaria",
            "order": 2
        },
        {
            "code": "TEC-03",
            "name": "Administración de Medicamentos",
            "description": "Precisión y seguridad en preparación, administración y registro de medicación",
            "order": 3
        },
        {
            "code": "TEC-04",
            "name": "Manejo de Equipamiento Médico",
            "description": "Competencia en operación y mantenimiento de equipos médicos especializados",
            "order": 4
        },
        {
            "code": "TEC-05",
            "name": "Cuidados Críticos y Urgencias",
            "description": "Capacidad de actuación rápida y efectiva en situaciones críticas y emergencias",
            "order": 5
        },
        {
            "code": "TEC-06",
            "name": "Registro y Documentación Clínica",
            "description": "Precisión y completitud en registros clínicos y documentación sanitaria",
            "order": 6
        },
        {
            "code": "TEC-07",
            "name": "Control de Signos Vitales",
            "description": "Exactitud en toma, interpretación y registro de signos vitales",
            "order": 7
        },
        {
            "code": "TEC-08",
            "name": "Técnicas de Curación y Vendajes",
            "description": "Destreza en curaciones, vendajes y cuidado de heridas",
            "order": 8
        },
        {
            "code": "TEC-09",
            "name": "Control de Infecciones",
            "description": "Aplicación efectiva de medidas de prevención y control de infecciones",
            "order": 9
        },
        {
            "code": "TEC-10",
            "name": "Educación al Paciente y Familia",
            "description": "Capacidad para educar e instruir a pacientes y familiares sobre cuidados",
            "order": 10
        },
        {
            "code": "TEC-11",
            "name": "Actualización y Formación Continua",
            "description": "Compromiso con actualización profesional y participación en capacitaciones",
            "order": 11
        }
    ]
    
    # 14 Attitudinal Criteria (Competencias Actitudinales)
    attitudinal_criteria = [
        {
            "code": "ACT-01",
            "name": "Responsabilidad Profesional",
            "description": "Compromiso con tareas asignadas, puntualidad y cumplimiento de obligaciones",
            "order": 12
        },
        {
            "code": "ACT-02",
            "name": "Trabajo en Equipo",
            "description": "Colaboración efectiva con colegas y otros profesionales de salud",
            "order": 13
        },
        {
            "code": "ACT-03",
            "name": "Comunicación Interpersonal",
            "description": "Claridad y efectividad en comunicación con pacientes, familias y equipo",
            "order": 14
        },
        {
            "code": "ACT-04",
            "name": "Empatía y Contención",
            "description": "Capacidad de comprensión y apoyo emocional a pacientes y familias",
            "order": 15
        },
        {
            "code": "ACT-05",
            "name": "Ética Profesional",
            "description": "Respeto por principios éticos, confidencialidad y derechos del paciente",
            "order": 16
        },
        {
            "code": "ACT-06",
            "name": "Adaptabilidad y Flexibilidad",
            "description": "Capacidad de adaptación a cambios, situaciones imprevistas y nuevas demandas",
            "order": 17
        },
        {
            "code": "ACT-07",
            "name": "Iniciativa y Proactividad",
            "description": "Anticipación de necesidades y propuesta de mejoras en procesos",
            "order": 18
        },
        {
            "code": "ACT-08",
            "name": "Manejo del Estrés",
            "description": "Control emocional y efectividad bajo presión y situaciones estresantes",
            "order": 19
        },
        {
            "code": "ACT-09",
            "name": "Respeto y Trato Digno",
            "description": "Trato respetuoso, cordial y digno hacia pacientes y compañeros",
            "order": 20
        },
        {
            "code": "ACT-10",
            "name": "Liderazgo y Supervisión",
            "description": "Capacidad de coordinar, guiar y supervisar cuando corresponda",
            "order": 21
        },
        {
            "code": "ACT-11",
            "name": "Compromiso Institucional",
            "description": "Identificación con valores y objetivos de la institución",
            "order": 22
        },
        {
            "code": "ACT-12",
            "name": "Resolución de Conflictos",
            "description": "Habilidad para mediar y resolver conflictos de manera constructiva",
            "order": 23
        },
        {
            "code": "ACT-13",
            "name": "Presentación Personal",
            "description": "Cuidado de imagen personal y cumplimiento de normas de vestimenta",
            "order": 24
        },
        {
            "code": "ACT-14",
            "name": "Disponibilidad y Compromiso Horario",
            "description": "Disponibilidad para cubrir necesidades del servicio y compromisos horarios",
            "order": 25
        }
    ]
    
    # Insert technical criteria
    for criteria_data in technical_criteria:
        criteria = Criteria(
            code=criteria_data["code"],
            name=criteria_data["name"],
            description=criteria_data["description"],
            criteria_type=CriteriaType.TECNICA,
            max_score=5,
            order=criteria_data["order"],
            is_active=True
        )
        db.add(criteria)
    
    # Insert attitudinal criteria
    for criteria_data in attitudinal_criteria:
        criteria = Criteria(
            code=criteria_data["code"],
            name=criteria_data["name"],
            description=criteria_data["description"],
            criteria_type=CriteriaType.ACTITUDINAL,
            max_score=5,
            order=criteria_data["order"],
            is_active=True
        )
        db.add(criteria)
    
    db.commit()
    print("Successfully seeded 25 evaluation criteria (11 technical + 14 attitudinal)")


def seed_admin_user(db: Session):
    """Create default admin user."""
    
    # Check if admin exists
    existing_admin = db.query(User).filter(User.username == "admin").first()
    if existing_admin:
        print("Admin user already exists")
        return
    
    admin_user = User(
        username="admin",
        email="admin@hospital.clinicas.uba.ar",
        full_name="Administrador del Sistema",
        hashed_password=get_password_hash("admin123"),
        role=RoleEnum.ADMIN,
        is_active=True
    )
    db.add(admin_user)
    db.commit()
    print("Created admin user (username: admin, password: admin123)")


def init_db():
    """Initialize database with seed data."""
    from app.db.session import SessionLocal
    
    db = SessionLocal()
    try:
        seed_criteria(db)
        seed_admin_user(db)
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
