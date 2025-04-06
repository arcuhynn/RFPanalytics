# 🧮 Evaluación de Proveedores para RFP Analítico

Esta aplicación, desarrollada con [Streamlit](https://streamlit.io/), permite evaluar proveedores de forma objetiva, visual e interactiva. Es ideal para procesos de licitación o RFPs (Request for Proposal) con múltiples participantes, como en entornos corporativos o gubernamentales.

---

##  Características principales

- ✅ Carga de archivos Excel con datos de proveedores (hasta cientos de registros).
- ✅ Evaluación automática basada en criterios ponderados.
- ✅ Cálculo del puntaje total y ranking general de proveedores.
- ✅ Visualización de **Top 10 y Bottom 10** por criterio en gráficas comparativas.
- ✅ Interfaz simple, pensada para usuarios de negocios o compras.
- 💡 Base sólida para integrarse con modelos de IA o análisis reputacional.

---

## Criterios de Evaluación

Los proveedores se evalúan según los siguientes criterios, con estos pesos por defecto:

| Criterio                         | Peso (%) |
|----------------------------------|----------|
| Precio                           | 20%      |
| Tiempo de entrega                | 10%      |
| Cumplimiento normativo           | 10%      |
| Estatus fiscal                   | 5%       |
| En lista negra                   | 5%       |
| Calidad del servicio             | 10%      |
| Capacidad de respuesta           | 10%      |
| Experiencia previa               | 10%      |
| Valor agregado                   | 5%       |
| Sostenibilidad                   | 5%       |
| Reputación externa               | 10%      |

---

##  Cómo ejecutar la app localmente

### 1. Clona este repositorio

```bash
git clone https://github.com/tuusuario/tu-repo.git
cd tu-repo
