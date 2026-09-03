# Reto de predicción de retornos en mercados de materias primas

## Contexto del problema

Las materias primas, también conocidas como commodities, son bienes físicos
obtenidos principalmente de la agricultura, la producción energética o la
extracción de recursos naturales, los cuales sirven como insumos para el
funcionamiento de distintas actividades económicas. Sin embargo, no todas
presentan el mismo comportamiento, debido a que sus precios dependen de
condiciones particulares como la disponibilidad del recurso, los ciclos de
producción, la capacidad de almacenamiento, la demanda industrial y los
acontecimientos geopolíticos. Según el Banco Mundial (2022), los mercados de
materias primas son esenciales para la economía global, pero difieren
considerablemente en los factores que determinan su oferta, demanda y
comportamiento de precios. Por esta razón, comprender sus movimientos es
relevante para empresas, inversionistas y gobiernos que dependen de estos
recursos para tomar decisiones.

El reto seleccionado busca anticipar retornos futuros a partir de datos
históricos provenientes de la London Metal Exchange, Japan Exchange Group, el
mercado de acciones de Estados Unidos y el mercado de divisas. Según Demkin et
al. (2025), combinar información de estos mercados puede contribuir a construir
pronósticos más estables y apoyar la gestión del riesgo en los mercados globales
de materias primas. Sin embargo, el problema no se limita a predecir el precio
de un solo producto, debido a que el dataset contiene múltiples variables
objetivo derivadas de los retornos futuros de distintos activos o de las
diferencias entre pares de activos. Esta diversidad aumenta la complejidad del
análisis, ya que las relaciones pueden variar según el instrumento, el mercado y
el horizonte temporal utilizado. Ante este escenario, el análisis exploratorio
permitirá comprender cómo se organizan los datos, qué patrones comparten las
variables y cuáles podrían aportar información para una futura etapa de
selección de características y modelado.

Debido a la cantidad de variables, mercados y objetivos presentes, este
problema puede abordarse mediante Ciencia de Datos, comenzando por un análisis
exploratorio que permita estudiar la información antes de establecer supuestos
o construir modelos. Heckert y Filliben (2003) explican que este tipo de
análisis busca obtener una mayor comprensión del conjunto de datos, descubrir
su estructura interna, identificar variables importantes y detectar valores
atípicos o anomalías. En este proyecto, dicho enfoque permitirá evaluar la
calidad de los datos y reconocer asociaciones entre instrumentos, mercados y
variables objetivo. De esta forma, los hallazgos obtenidos podrán servir como
fundamento para decidir qué relaciones y características convendría investigar
en una futura etapa predictiva.

## Situación problemática

La predicción de retornos en mercados de materias primas representa una
dificultad debido a que los instrumentos financieros no se comportan de forma
aislada, sino que pueden responder a cambios en la oferta y demanda,
acontecimientos económicos y movimientos de otros mercados. En el reto de
MITSUI&CO., esta complejidad aumenta por la combinación de información histórica
proveniente de la London Metal Exchange, Japan Exchange Group, el mercado de
acciones de Estados Unidos y el mercado de divisas, junto con 424 variables
objetivo construidas a partir de distintos activos, pares de activos y
horizontes temporales (Demkin et al., 2025). Aunque esta diversidad permite
estudiar el comportamiento conjunto de diferentes instrumentos, también
dificulta reconocer cuáles relaciones son relevantes y si estas se presentan de
manera consistente.

Por otro lado, contar con una gran cantidad de datos no garantiza que todas las
variables aporten información útil para una futura etapa predictiva. La
presencia de variables poco relacionadas con los objetivos, información
redundante o patrones inestables puede introducir ruido y aumentar
innecesariamente la complejidad del problema. Por esta razón, el análisis
exploratorio se centrará especialmente en examinar las asociaciones entre
predictores y variables objetivo, buscando reconocer cuáles presentan un mayor
potencial informativo y cuáles aparentemente aportan poca señal. Estos
resultados permitirán reducir el espacio de variables que deberá investigarse
posteriormente y establecer una base fundamentada para una futura selección de
características, sin afirmar todavía que su capacidad predictiva ha sido
comprobada mediante modelos.

## Problema científico

El dataset del MITSUI&CO. Commodity Prediction Challenge integra una gran
cantidad de variables procedentes de distintos mercados y 424 variables
objetivo (Demkin et al., 2025). Sin embargo, antes de desarrollar modelos
predictivos, se desconoce cuáles variables o familias de variables presentan
asociaciones más fuertes y consistentes con los objetivos, cuáles parecen
aportar información similar o repetida y cuáles muestran poca señal aparente.
Esta falta de conocimiento dificulta establecer, con base en evidencia, qué
variables deberían considerarse candidatas para una futura etapa de selección
de características.

## Pregunta de investigación

¿Qué variables y familias de variables presentan las asociaciones más fuertes
y consistentes con los objetivos del MITSUI&CO. Commodity Prediction Challenge,
y cuáles parecen aportar información similar o repetida a partir del análisis
exploratorio?

## Objetivos

### Objetivo general

Analizar la estructura, calidad y relaciones presentes en las variables del
dataset del MITSUI&CO. Commodity Prediction Challenge mediante técnicas de
análisis exploratorio, con el fin de establecer candidatos para una futura
selección de características.

### Objetivos específicos

- Evaluar la estructura y calidad del dataset mediante el análisis de sus tipos
  de datos, valores faltantes, duplicados y valores atípicos.

- Analizar el comportamiento estadístico y las distribuciones de las variables
  cuantitativas mediante medidas descriptivas y representaciones gráficas.

- Comparar las asociaciones entre variables predictoras, familias de variables
  y variables objetivo para reconocer relaciones relevantes dentro y entre los
  mercados representados.

- Clasificar las variables y familias de variables como candidatas con mayor
  potencial informativo, información similar o repetida, o poca señal aparente,
  con base en los resultados del análisis exploratorio.

## Referencias

Banco Mundial. (2022). *Commodity markets: Evolution, challenges, and
policies*. https://www.worldbank.org/en/research/publication/commodity-markets

Demkin, M., Takano, N., Rai, R., Dane, S., & Kitayama, T. (2025).
*MITSUI&CO. Commodity Prediction Challenge*. Kaggle.
https://www.kaggle.com/competitions/mitsui-commodity-prediction-challenge

Databento. (2024, 4 de marzo). *Working with high-frequency market data: Data
integrity and cleaning*. https://databento.com/blog/data-cleaning

Heckert, N. A., & Filliben, J. J. (2003). *NIST/SEMATECH e-Handbook of
Statistical Methods: Chapter 1, Exploratory Data Analysis*. National Institute
of Standards and Technology.
https://www.nist.gov/publications/nistsematech-e-handbook-statistical-methods-chapter-1-exploratory-data-analysis

Verousis, T., & ap Gwilym, O. (2010). An improved algorithm for cleaning ultra
high-frequency data. *Journal of Derivatives & Hedge Funds, 15*(4), 323–340.
https://doi.org/10.1057/jdhf.2009.16
