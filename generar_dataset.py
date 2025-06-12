import pandas as pd
import random
from faker import Faker
import numpy as np

fake = Faker()

# Número de entradas a generar
num_entries = 5000

# Listas auxiliares
grados = ['1ro', '2do', '3ro', '4to', '5to']
asignaturas = ['Matematicas', 'Lenguaje', 'Ciencias', 'Historia', 'Ingles']
docentes = [fake.name() for _ in range(10)]
estado_entrega_posibles = ['entregada a tiempo', 'tarde', 'no entregada']
tipo_falta_posibles = ['justificada', 'injustificada']
situacion_familiar_posibles = ['padres', 'madre sola', 'padre solo', 'tutor']
situacion_socioecon = ['baja', 'media', 'alta']

data = []

for i in range(num_entries):
    student_id = fake.uuid4()
    nombre_estudiante = fake.name()
    grado = random.choice(grados)
    asignatura = random.choice(asignaturas)
    docente = random.choice(docentes)
    nota_parcial_1 = round(random.uniform(1.0, 10.0), 1)
    nota_parcial_2 = round(random.uniform(1.0, 10.0), 1)
    nota_final = round((nota_parcial_1 + nota_parcial_2) / 2, 1)
    promedio_general = round(random.uniform(4.0, 10.0), 1)
    periodo = random.choice(['Trimestre 1', 'Trimestre 2', 'Trimestre 3'])
    fecha = fake.date_between(start_date='-90d', end_date='today')
    presente = random.choice([1, 0])
    tipo_falta = random.choice(tipo_falta_posibles) if not presente else ''
    tarea_id = fake.uuid4()
    fecha_entrega_programada = fake.date_between(start_date='-60d', end_date='today')
    fecha_entregada = fecha_entrega_programada if random.random() < 0.8 else fake.date_between(start_date=fecha_entrega_programada, end_date='+5d')
    estado_entrega = random.choices(estado_entrega_posibles, weights=[0.7, 0.2, 0.1])[0]
    cumplimiento_tareas = random.randint(40, 100)
    participacion = random.randint(0, 5)
    interacciones_lms = random.randint(0, 20)
    historial_reprobacion = random.randint(0, 3)
    nota_ultima_eval = round(random.uniform(1.0, 10.0), 1)
    asistencia_porcentaje = round(random.uniform(60.0, 100.0), 1)
    num_faltas_ultimos_30 = random.randint(0, 10)
    situacion_familiar = random.choice(situacion_familiar_posibles)
    situacion_socioecon = random.choice(situacion_socioecon)
    evaluacion_emocional = random.choice(['alta', 'media', 'baja'])

    data.append([
        student_id, nombre_estudiante, grado, asignatura, docente,
        nota_parcial_1, nota_parcial_2, nota_final, promedio_general, periodo,
        fecha, presente, tipo_falta,
        tarea_id, fecha_entrega_programada, fecha_entregada, estado_entrega,
        cumplimiento_tareas, participacion, interacciones_lms,
        historial_reprobacion, nota_ultima_eval, asistencia_porcentaje,
        num_faltas_ultimos_30, situacion_familiar, situacion_socioecon,
        evaluacion_emocional
    ])

# Columnas
columns = [
    'student_id', 'nombre_estudiante', 'grado', 'asignatura', 'docente',
    'nota_parcial_1', 'nota_parcial_2', 'nota_final', 'promedio_general', 'periodo_evaluacion',
    'fecha', 'presente', 'tipo_falta',
    'tarea_id', 'fecha_entrega_programada', 'fecha_entregada', 'estado_entrega',
    'cumplimiento_tareas_porcentaje', 'participacion_clase', 'interacciones_LMS',
    'historial_reprobacion', 'nota_ultima_evaluacion', 'asistencia_porcentaje',
    'numero_faltas_ultimos_30_dias', 'situacion_familiar', 'situacion_socioeconomica',
    'evaluacion_emocional'
]

# Crear DataFrame y exportar
df = pd.DataFrame(data, columns=columns)
df.to_csv("datos_kpi_escolares.csv", index=False)

print("Archivo CSV generado con éxito.")
