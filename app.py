import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Título de la app
st.title("Evaluación de Proveedores para RFP Analítico")

# Subida del archivo Excel
st.sidebar.header("Carga de datos")
archivo = st.sidebar.file_uploader("Sube el archivo Excel con datos de proveedores", type=["xlsx"])

if archivo is not None:
    df = pd.read_excel(archivo)
    st.subheader("Datos cargados")
    st.dataframe(df)

    # Asignar pesos (definidos previamente)
    pesos = {
        "Precio": 0.20,
        "Tiempo de entrega (días)": 0.10,
        "Cumple normativa": 0.10,
        "Estatus fiscal": 0.05,
        "En lista negra": 0.05,
        "Calidad del servicio": 0.10,
        "Capacidad de respuesta": 0.10,
        "Experiencia previa": 0.10,
        "Valor agregado": 0.05,
        "Sostenibilidad": 0.05,
        "Reputación externa": 0.10
    }

    # Normalización de datos y puntuación por criterio
    df_scored = df.copy()

    # Invertir valores para Precio y Tiempo de entrega (menos es mejor)
    df_scored["Precio_score"] = 1 - (df_scored["Precio"] - df_scored["Precio"].min()) / (df_scored["Precio"].max() - df_scored["Precio"].min())
    df_scored["Tiempo_score"] = 1 - (df_scored["Tiempo de entrega (días)"] - df_scored["Tiempo de entrega (días)"].min()) / (df_scored["Tiempo de entrega (días)"].max() - df_scored["Tiempo de entrega (días)"].min())

    # Convertir booleanos a numéricos para cálculo
    df_scored["Normativa_score"] = df_scored["Cumple normativa"].apply(lambda x: 1 if x == "Sí" else 0)
    df_scored["Fiscal_score"] = df_scored["Estatus fiscal"].apply(lambda x: 1 if x == "Al día" else 0)
    df_scored["Lista_negra_score"] = df_scored["En lista negra"].apply(lambda x: 0 if x == "Sí" else 1)

    # Puntajes ya están entre 1 y 10, los normalizamos a 0-1
    for col in ["Calidad del servicio", "Capacidad de respuesta", "Experiencia previa", "Valor agregado", "Sostenibilidad", "Reputación externa"]:
        df_scored[col + "_score"] = (df_scored[col] - 1) / 9

    # Cálculo de puntaje total ponderado
    df_scored["Score_total"] = (
        df_scored["Precio_score"] * pesos["Precio"] +
        df_scored["Tiempo_score"] * pesos["Tiempo de entrega (días)"] +
        df_scored["Normativa_score"] * pesos["Cumple normativa"] +
        df_scored["Fiscal_score"] * pesos["Estatus fiscal"] +
        df_scored["Lista_negra_score"] * pesos["En lista negra"] +
        df_scored["Calidad del servicio_score"] * pesos["Calidad del servicio"] +
        df_scored["Capacidad de respuesta_score"] * pesos["Capacidad de respuesta"] +
        df_scored["Experiencia previa_score"] * pesos["Experiencia previa"] +
        df_scored["Valor agregado_score"] * pesos["Valor agregado"] +
        df_scored["Sostenibilidad_score"] * pesos["Sostenibilidad"] +
        df_scored["Reputación externa_score"] * pesos["Reputación externa"]
    )

    # MODELO DE ML: Predicción de "Valor percibido"
    if "Valor percibido" in df_scored.columns and df_scored["Valor percibido"].notna().sum() > 5:
        st.subheader("🔍 Predicción de Valor Percibido (modelo entrenado)")

        # Separar datos con y sin etiqueta
        df_train = df_scored[df_scored["Valor percibido"].notna()]
        df_pred = df_scored[df_scored["Valor percibido"].isna()]

        features = [
            "Precio_score", "Tiempo_score", "Normativa_score", "Fiscal_score", "Lista_negra_score",
            "Calidad del servicio_score", "Capacidad de respuesta_score", "Experiencia previa_score",
            "Valor agregado_score", "Sostenibilidad_score", "Reputación externa_score"
        ]

        X = df_train[features]
        y = df_train["Valor percibido"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        if not df_pred.empty:
            df_scored.loc[df_pred.index, "Valor percibido estimado"] = model.predict(df_pred[features])

            st.success("Modelo entrenado con éxito y aplicado a proveedores sin historial.")

            # Mostrar top 10 por valor percibido estimado
            top_estimado = df_scored[df_scored["Valor percibido estimado"].notna()].copy()
            top_estimado = top_estimado[["Proveedor", "Valor percibido estimado"]].sort_values(
                by="Valor percibido estimado", ascending=False).head(10)

            st.markdown("### 🌟 Top 10 proveedores por valor percibido estimado")
            st.dataframe(top_estimado.style.background_gradient(cmap='Blues'))
        else:
            st.info("Todos los proveedores ya tienen historial de valor percibido. No se aplicó predicción.")

    # RESUMEN EJECUTIVO
    st.subheader("Resumen Ejecutivo")
    st.metric("Número de proveedores evaluados", len(df_scored))
    st.metric("Puntaje promedio general", round(df_scored["Score_total"].mean(), 2))
    st.metric("Mejor proveedor", df_scored.loc[df_scored["Score_total"].idxmax(), "Proveedor"])
    st.metric("Peor proveedor", df_scored.loc[df_scored["Score_total"].idxmin(), "Proveedor"])

    fig_hist = px.histogram(df_scored, x="Score_total", nbins=20, title="Distribución de Puntajes Generales")
    st.plotly_chart(fig_hist)

    # Mostrar ranking
    st.subheader("Ranking de proveedores")
    ranking = df_scored[["Proveedor", "Score_total"]].sort_values(by="Score_total", ascending=False).reset_index(drop=True)
    st.dataframe(ranking.style.background_gradient(cmap='Greens'))

    # Visualización: Top y Bottom 10 por criterio con Plotly
    st.subheader("Comparativo Interactivo de Top 10 y Bottom 10 por criterio")

    criterios_visuales = {
        "Precio": "Precio",
        "Tiempo de entrega (días)": "Tiempo de entrega (días)",
        "Calidad del servicio": "Calidad del servicio",
        "Capacidad de respuesta": "Capacidad de respuesta",
        "Experiencia previa": "Experiencia previa",
        "Valor agregado": "Valor agregado",
        "Sostenibilidad": "Sostenibilidad",
        "Reputación externa": "Reputación externa"
    }

    for criterio, columna in criterios_visuales.items():
        st.markdown(f"### {criterio}")

        top10 = df_scored.nlargest(10, columna)[["Proveedor", columna]].sort_values(by=columna, ascending=True)
        fig_top = px.bar(top10, x=columna, y="Proveedor", orientation="h", title=f"Top 10 proveedores por {criterio}", color=columna)
        st.plotly_chart(fig_top)

        bottom10 = df_scored.nsmallest(10, columna)[["Proveedor", columna]].sort_values(by=columna, ascending=True)
        fig_bottom = px.bar(bottom10, x=columna, y="Proveedor", orientation="h", title=f"Bottom 10 proveedores por {criterio}", color=columna)
        st.plotly_chart(fig_bottom)
    # Exportar resultados con predicción y score total
    st.subheader("📥 Descargar resultados procesados")

    from io import BytesIO

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_scored.to_excel(writer, sheet_name='Resultados', index=False)
        writer.save()
    processed_data = output.getvalue()

    st.download_button(
        label="Descargar archivo Excel con resultados",
        data=processed_data,
        file_name="Evaluacion_Proveedores_Procesada.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("Por favor, sube un archivo Excel para comenzar.")

