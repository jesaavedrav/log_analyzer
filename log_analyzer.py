import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict

# Define log data structure
error_logs = {
    "Conexión": [
        "Could not connect to: {configuración}",
        "Invalid configuration: {configuración}",
        "Connection setup failed to context {contexto}!",
        "Failed commiting read session on queue {nombre_cola}",
        "Sending failed to {nombre_cola}!",
        "Error while receiving from {nombre_cola}",
        "Error while receiving from {nombre_cola} The node will stop.",
        "Rollback failed"
    ],
    "Archivo": [
        "Invalid file format!",
        "Error reading bytes message >>> {mensaje}",
        "Error reading file content (file = {nombre_archivo})",
        "Unknown message type!!!"
    ],
    "Control": [
        "START request will be ignored for node [{nodo}] which has a pending start request, control point [{punto_control}]",
        "Error retrieving participant data from form",
        "Received null participant data (id) for validating",
        "Received invalid participant for validating"
    ]
}

warning_logs = {
    "Configuración": [
        "Failed parsing log message size limit ({valor}). Will default to none!",
        "Ignoring message size limit ({valor}). Cannot be smaller than 1000. Will default to none!",
        "Failed parsing minimum commit ({valor}). Will default to {valor_default}",
        "Ignoring message size limit ({valor}). Cannot be smaller than 1 or greater than 100. Will default to 1",
        "Ignoring message mininum time commit ({valor}). Will default to {valor_default}"
    ]
}

def create_error_distribution_chart():
    # Create data for error distribution
    error_counts = {category: len(messages) for category, messages in error_logs.items()}
    # Preprocesar los mensajes para mostrar solo la parte antes de '{'
    processed_error_logs = {cat: [msg.split('{')[0] for msg in msgs] for cat, msgs in error_logs.items()}
    # Create pie chart using plotly
    fig = go.Figure(data=[go.Pie(
        labels=list(error_counts.keys()),
        values=list(error_counts.values()),
        hole=.3
    )])
    fig.update_layout(
        title="Distribución de Errores por Categoría",
        annotations=[dict(text='Errores', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    fig.show()

def create_severity_comparison():
    # Preprocesar los mensajes para mostrar solo la parte antes de '{'
    processed_error_logs = {cat: [msg.split('{')[0] for msg in msgs] for cat, msgs in error_logs.items()}
    processed_warning_logs = {cat: [msg.split('{')[0] for msg in msgs] for cat, msgs in warning_logs.items()}
    # Prepare data
    error_total = sum(len(msgs) for msgs in processed_error_logs.values())
    warning_total = sum(len(msgs) for msgs in processed_warning_logs.values())
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=['ERROR', 'WARNING'],
            y=[error_total, warning_total],
            text=[error_total, warning_total],
            textposition='auto',
        )
    ])
    fig.update_layout(
        title="Comparación de Mensajes por Nivel de Severidad",
        xaxis_title="Nivel de Severidad",
        yaxis_title="Cantidad de Mensajes",
        template='plotly_white'
    )
    fig.show()

def create_detailed_category_analysis():
    # Preprocesar los mensajes para mostrar solo la parte antes de '{'
    processed_error_logs = {cat: [msg.split('{')[0] for msg in msgs] for cat, msgs in error_logs.items()}
    processed_warning_logs = {cat: [msg.split('{')[0] for msg in msgs] for cat, msgs in warning_logs.items()}
    # Prepare data
    categories = []
    message_counts = []
    severity_types = []
    for category, messages in processed_error_logs.items():
        categories.extend([category] * len(messages))
        message_counts.extend([len(messages)] * len(messages))
        severity_types.extend(['ERROR'] * len(messages))
    for category, messages in processed_warning_logs.items():
        categories.extend([category] * len(messages))
        message_counts.extend([len(messages)] * len(messages))
        severity_types.extend(['WARNING'] * len(messages))
    df = pd.DataFrame({
        'Categoría': categories,
        'Cantidad': message_counts,
        'Severidad': severity_types
    })
    fig = px.treemap(df,
                     path=[px.Constant("Todos los Mensajes"), 'Severidad', 'Categoría'],
                     values='Cantidad',
                     color='Severidad',
                     color_discrete_map={'ERROR': '#ff6b6b', 'WARNING': '#ffd93d'})
    fig.update_layout(
        title="Análisis Detallado por Categoría y Severidad"
    )
    fig.show()

def create_error_histogram():
    # Preprocesar los mensajes para mostrar solo la parte antes de '{'
    processed_error_msgs = []
    for msgs in error_logs.values():
        processed_error_msgs.extend([msg.split('{')[0].strip() for msg in msgs])
    # Crear histograma de frecuencias
    df = pd.DataFrame({'Mensaje': processed_error_msgs})
    fig = px.histogram(df, x='Mensaje', color_discrete_sequence=['#ff6b6b'])
    fig.update_layout(title="Histograma de Frecuencias de Errores", xaxis_title="Mensaje de Error", yaxis_title="Frecuencia")
    fig.show()

def create_warning_histogram():
    # Preprocesar los mensajes para mostrar solo la parte antes de '{'
    processed_warning_msgs = []
    for msgs in warning_logs.values():
        processed_warning_msgs.extend([msg.split('{')[0].strip() for msg in msgs])
    # Crear histograma de frecuencias
    df = pd.DataFrame({'Mensaje': processed_warning_msgs})
    fig = px.histogram(df, x='Mensaje', color_discrete_sequence=['#ffd93d'])
    fig.update_layout(title="Histograma de Frecuencias de Warnings", xaxis_title="Mensaje de Warning", yaxis_title="Frecuencia")
    fig.show()

def main():
    # Create all visualizations
    create_error_distribution_chart()
    create_severity_comparison()
    create_detailed_category_analysis()
    create_error_histogram()
    create_warning_histogram()

    print("Análisis completado. Se han mostrado los gráficos en pantalla.")
    print("1. Distribución de errores por categoría")
    print("2. Comparación de mensajes por severidad")
    print("3. Análisis detallado por categoría y severidad")
    print("4. Histograma de frecuencias de errores")
    print("5. Histograma de frecuencias de warnings")

if __name__ == "__main__":
    main()
