export type RubricItem = {
  key: string;
  name: string;
  type: "technical" | "attitude";
};

export const RUBRIC_ITEMS: RubricItem[] = [
  { key: "CT1", name: "Cuidado de Heridas y Curaciones", type: "technical" },
  { key: "CT2", name: "Administración de Medicamentos", type: "technical" },
  { key: "CT3", name: "Monitorío de Signos Vitales", type: "technical" },
  { key: "CT4", name: "Higiene y Confort del Paciente", type: "technical" },
  { key: "CT5", name: "Registro en Historia Clínica", type: "technical" },
  { key: "CT6", name: "Comunicación con Equipo Médico", type: "technical" },
  { key: "CT7", name: "Conocimiento de Patologías Comunes", type: "technical" },
  { key: "CT8", name: "Manejo de Equipos Médicos", type: "technical" },
  { key: "CT9", name: "Acción ante Emergencias", type: "technical" },
  { key: "CT10", name: "Prevención de Infecciones", type: "technical" },
  { key: "CT11", name: "Manejo de Drenajes y Catéteres", type: "technical" },
  { key: "CA12", name: "Responsabilidad y Puntualidad", type: "attitude" },
  { key: "CA13", name: "Actitud hacia el Paciente", type: "attitude" },
  { key: "CA14", name: "Trabajo en Equipo", type: "attitude" },
  { key: "CA15", name: "Capacidad de Aprendizaje", type: "attitude" },
  { key: "CA16", name: "Iniciativa y Proactividad", type: "attitude" },
  { key: "CA17", name: "Comunicación Efectiva", type: "attitude" },
  { key: "CA18", name: "Confidencialidad", type: "attitude" },
  { key: "CA19", name: "Cumplimiento de Normas", type: "attitude" },
  { key: "CA20", name: "Manejo del Estrés", type: "attitude" },
  { key: "CA21", name: "Orientación al Paciente", type: "attitude" },
  { key: "CA22", name: "Ética Profesional", type: "attitude" },
  { key: "CA23", name: "Liderazgo en Sala", type: "attitude" },
  { key: "CA24", name: "Manejo de Conflictos", type: "attitude" },
  { key: "CA25", name: "Compromiso Institucional", type: "attitude" }
];
