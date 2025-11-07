# Simulador GPS — Algoritmos de Dijkstra y Bellman-Ford

Este programa es una aplicación con interfaz gráfica que permite crear y simular grafos dirigidos, mostrando cómo funcionan los algoritmos de **Dijkstra** y **Bellman-Ford** para encontrar el camino más corto entre dos puntos.  
Se pueden agregar nodos, conectarlos con pesos personalizados y visualizar los resultados directamente en pantalla.

---

## Características principales

- Permite **crear nodos** haciendo clic en el lienzo.  
- Se pueden **conectar los nodos** indicando el peso de cada arista.  
- Muestra el **camino más corto** con un color diferente.  
- Ofrece dos algoritmos de cálculo:
  - Dijkstra (para grafos sin pesos negativos)
  - Bellman-Ford (permite pesos negativos)
- Incluye una opción para **comparar el rendimiento** de ambos algoritmos.  
- Se puede **guardar** y **cargar** grafos en formato JSON.  
- Permite **exportar una imagen** del grafo en formato PNG.  
- Incluye botones para **limpiar** todo y empezar de nuevo.

---

## Requisitos

Antes de ejecutar el programa, asegúrate de tener instalado **Python 3.8 o superior**.  
También es necesario tener las siguientes librerías:

```bash
pip install networkx matplotlib
```

Tkinter viene incluido con Python en la mayoría de los sistemas, pero si no lo tienes:

```bash
sudo apt-get install python3-tk
```

---

## Cómo usarlo

1. Ejecuta el archivo principal:

   ```bash
   python dijkstra.py
   ```

2. En la ventana que se abre:
   - Usa los botones de modo para agregar nodos o conectarlos.  
   - Escribe el peso de la arista en el campo correspondiente.  
   - Define los nodos de **origen** y **destino** (también puedes seleccionarlos haciendo clic).  
   - Haz clic en **Ejecutar Dijkstra** o **Ejecutar Bellman-Ford** para calcular el camino más corto.  
   - Usa **Comparar rendimiento** para ver qué algoritmo es más rápido.  

3. Puedes guardar el grafo, cargar otro o exportar la imagen en cualquier momento.

---

## Ejemplo rápido

1. Agrega tres nodos: `A`, `B` y `C`.  
2. Conéctalos así:
   - A → B con peso 2  
   - B → C con peso 3  
   - A → C con peso 6  
3. Define `A` como origen y `C` como destino.  
4. Ejecuta **Dijkstra**.  
   Verás que el camino más corto es **A → B → C** con una distancia total de **5**.

---

## Formato de los archivos guardados

Cuando guardas un grafo, se crea un archivo `.json` con una estructura similar a esta:

```json
{
  "nodos": {"A": [100, 200], "B": [300, 200]},
  "aristas": {"A": {"B": 2}, "B": {}}
}
```

---

## Notas finales

El programa fue pensado como una herramienta educativa para visualizar cómo trabajan los algoritmos de caminos más cortos.  
Es útil para practicar grafos, entender el funcionamiento de Dijkstra y Bellman-Ford y comparar su desempeño en distintos escenarios.
