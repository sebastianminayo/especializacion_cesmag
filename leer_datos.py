import pandas as pd
import os

# 1. Obtener la ruta de la carpeta donde está este script (.py)
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
nombre_archivo = 'datos_sinteticos.csv'
ruta_completa = os.path.join(carpeta_actual, nombre_archivo)

print(f"Buscando el archivo en: {ruta_completa}")

try:
    # 2. Cargar los datos usando la ruta absoluta
    df = pd.read_csv(ruta_completa)
    print("✅ ¡Archivo cargado con éxito!\n")

    # --- ANÁLISIS RÁPIDO ---
    # Convertir fecha
    df['fecha_campana'] = pd.to_datetime(df['fecha_campana'])

    # Rendimiento por Plataforma
    resumen = df.groupby('plataforma').agg({
        'costo_total': 'sum',
        'revenue_generado': 'sum',
        'roas': 'mean'
    }).reset_index()

    print("--- RESUMEN POR PLATAFORMA ---")
    print(resumen)

except FileNotFoundError:
    print(f"❌ ERROR: No se encontró el archivo '{nombre_archivo}'.")
    print(f"Asegúrate de que el archivo CSV esté dentro de la carpeta:")
    print(f"👉 {carpeta_actual}")
except Exception as e:
    print(f"❌ Ocurrió un error inesperado: {e}")

    # --- MÓDULO: ANÁLISIS CRUZADO ---
print("\n--- MATRIZ PLATAFORMA VS AUDIENCIA (ROAS PROMEDIO) ---")
pivot_audiencia = df.pivot_table(
    index='plataforma', 
    columns='audiencia_objetivo', 
    values='roas', 
    aggfunc='mean'
).fillna(0) # Rellena con 0 si no hay datos para esa combinación

print(pivot_audiencia)

# Tip: Las audiencias con ROAS > 2 suelen ser las más rentables.
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. CONFIGURACIÓN DE RUTA ---
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
nombre_archivo = 'datos_sinteticos.csv'
ruta_completa = os.path.join(carpeta_actual, nombre_archivo)

if os.path.exists(ruta_completa):
    df = pd.read_csv(ruta_completa)
    df['fecha_campana'] = pd.to_datetime(df['fecha_campana'])
    
    # Configuramos el estilo de las gráficas
    sns.set_theme(style="whitegrid")
    
    

    # --- 3. GRÁFICA: CPC VS TASA DE CONVERSIÓN ---
    # ¿Pagar más por el click nos asegura más ventas?
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='cpc', y='conversion_rate', hue='plataforma', size='presupuesto_diario', sizes=(20, 200))
    plt.title('Relación: Costo por Clic vs. Tasa de Conversión', fontsize=14)
    plt.xlabel('Costo por Clic (CPC)')
    plt.ylabel('Tasa de Conversión (%)')
    plt.savefig('cpc_vs_conversion.png')
    print("✅ Gráfica de Correlación guardada como 'cpc_vs_conversion.png'")

    # --- 4. INSIGHT: MATRIZ DE CORRELACIÓN ---
    # Esto nos dice qué métricas están conectadas entre sí
    print("\n--- INSIGHTS DE CORRELACIÓN ---")
    # Seleccionamos solo columnas numéricas
    cols_interes = ['presupuesto_diario', 'impresiones', 'clicks', 'conversiones', 'costo_total', 'revenue_generado', 'roas']
    matriz_corr = df[cols_interes].corr()
    
    # Imprimimos la correlación con el Revenue
    corr_revenue = matriz_corr['revenue_generado'].sort_values(ascending=False)
    print("Correlación con los Ingresos Generados:")
    print(corr_revenue)

    # --- 5. INSIGHT: EFICIENCIA DE AUDIENCIA ---
    # Buscamos la audiencia con el menor CPA (Costo por Adquisición)
    print("\n--- MEJORES AUDIENCIAS POR COSTO DE ADQUISICIÓN (CPA) ---")
    cpa_audiencia = df.groupby('audiencia_objetivo')['cpa'].mean().sort_values()
    print(cpa_audiencia)

else:
    print(f"No se encontró el archivo en: {ruta_completa}")

    import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Configuración de ruta y carga de datos
# Asegúrate de que el archivo esté en la misma carpeta que este script
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_csv = os.path.join(carpeta_actual, 'datos_sinteticos.csv')

try:
    df = pd.read_csv(ruta_csv)
    df['fecha_campana'] = pd.to_datetime(df['fecha_campana'])

    # Configuración estética
    sns.set_theme(style="whitegrid", palette="muted")
    
    # Crear la figura con 4 espacios (2 filas, 2 columnas)
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Dashboard de Insights: Rendimiento de Marketing', fontsize=22, fontweight='bold', y=0.98)

    # --- GRÁFICA 1: ROAS por Plataforma ---
    # Identifica qué canal es más rentable
    sns.barplot(ax=axes[0, 0], data=df, x='plataforma', y='roas', palette='viridis', ci=None)
    axes[0, 0].set_title('Retorno de Inversión (ROAS) por Plataforma', fontsize=14, pad=10)
    axes[0, 0].axhline(1, color='red', linestyle='--', alpha=0.7, label='Equilibrio (1.0)')
    axes[0, 0].set_ylabel('ROAS Promedio')

    # --- GRÁFICA 2: Presupuesto vs Revenue ---
    # Muestra si invertir más realmente genera más ventas (Tendencia)
    sns.regplot(ax=axes[0, 1], data=df, x='presupuesto_diario', y='revenue_generado', 
                scatter_kws={'alpha':0.6}, line_kws={'color':'orange'})
    axes[0, 1].set_title('Escalabilidad: Presupuesto vs. Revenue', fontsize=14, pad=10)
    axes[0, 1].set_xlabel('Presupuesto Diario ($)')
    axes[0, 1].set_ylabel('Revenue Generado ($)')

    # --- GRÁFICA 3: Engagement por Audiencia ---
    # Compara qué grupos de edad interactúan más
    sns.boxplot(ax=axes[1, 0], data=df, x='audiencia_objetivo', y='engagement_rate', palette='Set2')
    axes[1, 0].set_title('Calidad del Anuncio: Engagement por Audiencia', fontsize=14, pad=10)
    axes[1, 0].set_ylabel('Engagement Rate (%)')

    # --- GRÁFICA 4: CPA por Objetivo ---
    # Cuánto cuesta una conversión según el tipo de campaña
    sns.barplot(ax=axes[1, 1], data=df, x='tipo_campana', y='cpa', palette='magma', ci=None)
    axes[1, 1].set_title('Eficiencia: Costo por Adquisición (CPA) por Objetivo', fontsize=14, pad=10)
    axes[1, 1].set_ylabel('CPA Promedio ($)')

    # Ajuste final de diseño
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Guardar la imagen final
    nombre_salida = 'dashboard_marketing_final.png'
    plt.savefig(nombre_salida, dpi=300) # dpi=300 para alta calidad
    print(f"✅ Dashboard generado exitosamente: {nombre_salida}")
    
except FileNotFoundError:
    print("❌ No se encontró 'datos_sinteticos.csv'. Verifica que esté en la misma carpeta que el script.")


    