# Diseno de la inspeccion inicial del dataset

## Decision general

El analisis exploratorio se desarrollara progresivamente en un unico notebook:
`notebooks/01_analisis_exploratorio.ipynb`. Cada tarea posterior agregara una
seccion nueva, de modo que el trabajo conserve un hilo continuo y no duplique
la carga de datos.

## Alcance de la primera seccion

La primera seccion respondera la pregunta: **que datos tenemos realmente y
como estan organizados?** Su alcance se limita a la inspeccion y descripcion
inicial. No evaluara valores faltantes, duplicados, outliers ni posibles
decisiones de limpieza.

## Contenido aprobado

1. Presentar el proposito y los limites de la inspeccion.
2. Explicar por que el reto utiliza varios archivos en lugar de un solo CSV y
   describir la funcion de `train.csv`, `train_labels.csv`, `target_pairs.csv`
   y `test.csv`.
3. Mostrar como se relacionan los cuatro archivos mediante `date_id`, los
   nombres `target_0` a `target_423` y la metadata de `target_pairs.csv`.
4. Cargar los archivos originales desde `data/raw/` sin modificarlos.
5. Construir un inventario con el numero de filas, columnas y rango de
   `date_id` de cada archivo.
6. Identificar predictores, variables objetivo, identificadores y variables
   auxiliares.
7. Resumir los tipos de datos sin entrar todavia en el diagnostico de calidad.
8. Clasificar los predictores segun el mercado indicado por su nomenclatura:
   LME, JPX, acciones de Estados Unidos y divisas.
9. Resumir la estructura de los targets segun su rezago y la composicion
   indicada en `target_pairs.csv`.
10. Cerrar con una sintesis interpretativa breve.

## Enfoque tecnico

Se utilizara una inspeccion estructurada basada en funciones pequenas para
producir tablas resumidas. Este enfoque evita imprimir manualmente cientos de
columnas y deja componentes reutilizables para las siguientes secciones del
EDA. El notebook solo mostrara resultados; no escribira en `data/raw/` ni
generara una version procesada del dataset.

## Criterios de aceptacion

- El notebook se ejecuta de principio a fin sin modificar los archivos crudos.
- Los cuatro CSV se cargan correctamente mediante rutas relativas al proyecto.
- La relacion entre los archivos queda explicada para una persona acostumbrada
  a trabajar con un solo CSV.
- Las 558 columnas de `train.csv` se resumen de forma util y no como una lista
  extensa sin interpretacion.
- La seccion no adelanta el diagnostico de calidad ni el preprocesamiento.
