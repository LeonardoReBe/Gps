import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import time
import json
from PIL import Image, ImageTk
class GPSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador GPS - Dijkstra y Bellman-Ford")
        self.canvas = tk.Canvas(root, width=800, height=500, bg="white")
        self.canvas.pack()
        # Cargar imagen de fondo
        imagen = Image.open("mapa.png")  # Cambia "fondo.png" por el nombre de tu archivo
        imagen = imagen.resize((800, 500))  # Ajusta al tamaño del canvas
        self.imagen_fondo_tk = ImageTk.PhotoImage(imagen)
        self.canvas.create_image(0, 0, image=self.imagen_fondo_tk, anchor="nw")

        self.nodos = {}  # nombre → (x, y)
        self.aristas = {}  # nombre → {vecino: peso}
        self.modo = tk.StringVar(value="Agregar nodo")
        self.seleccion = []

        # Selector de modo
        modos = [
            "Agregar nodo",
            "Conectar nodos",
            "Editar nombre",
            "Eliminar nodo",
            "Eliminar arista",
            "Seleccionar origen/destino"
        ]
        modo_frame = tk.Frame(root)
        modo_frame.pack()
        for m in modos:
            tk.Radiobutton(modo_frame, text=m, variable=self.modo, value=m).pack(side="left", padx=5)

        # Entradas de peso, origen y destino
        entrada_frame = tk.Frame(root)
        entrada_frame.pack(pady=5)

        self.peso_entry = tk.Entry(entrada_frame, width=20)
        self.peso_entry.pack(side="left", padx=5)
        self.peso_entry.insert(0, "Peso de la arista")

        self.origen_entry = tk.Entry(entrada_frame, width=20)
        self.origen_entry.pack(side="left", padx=5)
        self.origen_entry.insert(0, "Nodo origen")

        self.destino_entry = tk.Entry(entrada_frame, width=20)
        self.destino_entry.pack(side="left", padx=5)
        self.destino_entry.insert(0, "Nodo destino")

        # Botones en dos columnas
        boton_frame = tk.Frame(root)
        boton_frame.pack(pady=5)

        botones = [
            ("Ejecutar Dijkstra", self.ejecutar_dijkstra),
            ("Ejecutar Bellman-Ford", self.ejecutar_bellman_ford),
            ("Comparar rendimiento", self.comparar_rendimiento),
            ("Guardar grafo", self.guardar_grafo),
            ("Cargar grafo", self.cargar_grafo),
            ("Exportar imagen", self.exportar_imagen),
            ("Visualizar grafo", self.visualizar_grafo),
            ("Limpiar todo", self.limpiar)
        ]

        for i, (texto, comando) in enumerate(botones):
            tk.Button(boton_frame, text=texto, command=comando, width=20).grid(row=i//2, column=i%2, padx=5, pady=2)

        # Vincular clic en el canvas
        self.canvas.bind("<Button-1>", self.interaccion)
    def interaccion(self, event):
        modo = self.modo.get()
        if modo == "Agregar nodo":
            self.agregar_nodo(event)
        elif modo == "Conectar nodos":
            self.seleccionar_para_conectar(event)
        elif modo == "Editar nombre":
            self.editar_nodo(event)
        elif modo == "Eliminar nodo":
            self.eliminar_nodo(event)
        elif modo == "Eliminar arista":
            self.eliminar_arista(event)
        elif modo == "Seleccionar origen/destino":
            self.seleccionar_origen_destino(event)
    def agregar_nodo(self, event):
        nombre = simpledialog.askstring("Nombre del nodo", "Ingresa el nombre del nodo:")
        if not nombre or nombre in self.nodos:
            return
        x, y = event.x, event.y
        self.nodos[nombre] = (x, y)
        self.aristas[nombre] = {}
        self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="lightblue", tags=nombre)
        self.canvas.create_text(x, y, text=nombre, tags=nombre)

    def seleccionar_para_conectar(self, event):
        for nombre, (x, y) in self.nodos.items():
            if abs(event.x - x) < 20 and abs(event.y - y) < 20:
                self.seleccion.append(nombre)
                if len(self.seleccion) == 2:
                    self.conectar_nodos()
                break

    def conectar_nodos(self):
        origen, destino = self.seleccion
        try:
            peso = float(self.peso_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Peso inválido.")
            self.seleccion = []
            return
        self.aristas[origen][destino] = peso
        x1, y1 = self.nodos[origen]
        x2, y2 = self.nodos[destino]
        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, tags=f"{origen}_{destino}")
        self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(peso), tags=f"{origen}_{destino}")
        self.seleccion = []

    def editar_nodo(self, event):
        for nombre, (x, y) in self.nodos.items():
            if abs(event.x - x) < 20 and abs(event.y - y) < 20:
                nuevo = simpledialog.askstring("Editar nombre", f"Nuevo nombre para '{nombre}':")
                if nuevo and nuevo not in self.nodos:
                    self.nodos[nuevo] = self.nodos.pop(nombre)
                    self.aristas[nuevo] = self.aristas.pop(nombre)
                    for vecino in self.aristas:
                        if nombre in self.aristas[vecino]:
                            self.aristas[vecino][nuevo] = self.aristas[vecino].pop(nombre)
                    self.canvas.delete(nombre)
                    self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="lightblue", tags=nuevo)
                    self.canvas.create_text(x, y, text=nuevo, tags=nuevo)
                break

    def eliminar_nodo(self, event):
        for nombre, (x, y) in self.nodos.items():
            if abs(event.x - x) < 20 and abs(event.y - y) < 20:
                self.canvas.delete(nombre)
                for vecino in self.aristas[nombre]:
                    self.canvas.delete(f"{nombre}_{vecino}")
                for origen in self.aristas:
                    if nombre in self.aristas[origen]:
                        self.canvas.delete(f"{origen}_{nombre}")
                        del self.aristas[origen][nombre]
                del self.aristas[nombre]
                del self.nodos[nombre]
                break

    def eliminar_arista(self, event):
        for origen in self.aristas:
            for destino in self.aristas[origen]:
                x1, y1 = self.nodos[origen]
                x2, y2 = self.nodos[destino]
                if abs(event.x - (x1 + x2) // 2) < 20 and abs(event.y - (y1 + y2) // 2) < 20:
                    self.canvas.delete(f"{origen}_{destino}")
                    del self.aristas[origen][destino]
                    return
                
    def dijkstra(self, graph, start):
        dist = {node: float('inf') for node in graph}
        dist[start] = 0
        pred = {node: None for node in graph}
        queue = [(0, start)]
        while queue:
            d, u = heapq.heappop(queue)
            for v, w in graph[u].items():
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    pred[v] = u
                    heapq.heappush(queue, (dist[v], v))
        return dist, pred
    def ejecutar_bellman_ford(self):
        origen = self.origen_entry.get().strip()
        destino = self.destino_entry.get().strip()
        if origen not in self.nodos or destino not in self.nodos:
            messagebox.showerror("Error", "Nodos inválidos.")
            return
        distancias, predecesores = self.bellman_ford(self.aristas, origen)
        camino = self.reconstruir_camino(predecesores, destino, origen)
        if not camino:
            messagebox.showinfo("Resultado", "No hay camino.")
        else:
            texto = f"Distancia: {distancias[destino]}\nCamino: {' → '.join(camino)}"
            messagebox.showinfo("Bellman-Ford", texto)
            self.visualizar_grafo(camino, origen, destino)
    def ejecutar_dijkstra(self):
        origen = self.origen_entry.get().strip()
        destino = self.destino_entry.get().strip()
        if origen not in self.nodos or destino not in self.nodos:
            messagebox.showerror("Error", "Nodos inválidos.")
            return
        distancias, predecesores = self.dijkstra(self.aristas, origen)
        camino = self.reconstruir_camino(predecesores, destino, origen)
        if not camino:
            messagebox.showinfo("Resultado", "No hay camino.")
        else:
            texto = f"Distancia: {distancias[destino]}\nCamino: {' → '.join(camino)}"
            messagebox.showinfo("Dijkstra", texto)
            self.visualizar_grafo(camino, origen, destino)
    def bellman_ford(self, graph, start):
        dist = {node: float('inf') for node in graph}
        dist[start] = 0
        pred = {node: None for node in graph}
        for _ in range(len(graph) - 1):
            for u in graph:
                for v, w in graph[u].items():
                    if dist[u] + w < dist[v]:
                        dist[v] = dist[u] + w
                        pred[v] = u
        return dist, pred

    def reconstruir_camino(self, pred, end, start):
        path = []
        current = end
        while current is not None:
            path.append(current)
            if current == start:
                break
            current = pred[current]
        path.reverse()
        return path if path and path[0] == start else []

    def visualizar_grafo(self, camino=None, start=None, end=None):
        G = nx.DiGraph()
        for origen in self.aristas:
            for destino, peso in self.aristas[origen].items():
                G.add_edge(origen, destino, weight=peso)

        pos = self.nodos
        node_colors = []
        for nodo in G.nodes():
            if nodo == start:
                node_colors.append("green")
            elif nodo == end:
                node_colors.append("red")
            else:
                node_colors.append("lightblue")

        nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, arrows=True)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        if camino:
            aristas_camino = list(zip(camino[:-1], camino[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=aristas_camino, edge_color='pink', width=3)

        plt.title(f"Camino más corto de {start} a {end}" if camino else "Grafo completo")
        plt.show()
    def comparar_rendimiento(self):
        if len(self.nodos) < 2 or not any(self.aristas.values()):
            messagebox.showwarning("Comparación", "Dibuja al menos dos nodos conectados para comparar rendimiento.")
            return

        origen = self.origen_entry.get().strip()
        if origen not in self.nodos:
            messagebox.showerror("Error", "Debes ingresar un nodo de origen válido.")
            return

        inicio_dijkstra = time.time()
        dist_d, _ = self.dijkstra(self.aristas, origen)
        tiempo_dijkstra = time.time() - inicio_dijkstra

        inicio_bf = time.time()
        dist_bf, _ = self.bellman_ford(self.aristas, origen)
        tiempo_bellman = time.time() - inicio_bf

        plt.bar(["Dijkstra", "Bellman-Ford"], [tiempo_dijkstra, tiempo_bellman], color=["blue", "orange"])
        plt.ylabel("Tiempo (segundos)")
        plt.title(f"Comparación de rendimiento en tu grafo ({len(self.nodos)} nodos)")
        plt.show()
    def guardar_grafo(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not archivo:
            return
        datos = {
            "nodos": self.nodos,
            "aristas": self.aristas
        }
        with open(archivo, "w") as f:
            json.dump(datos, f)
        messagebox.showinfo("Guardado", "Grafo guardado correctamente.")

    def cargar_grafo(self):
        archivo = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not archivo:
            return
        with open(archivo, "r") as f:
            datos = json.load(f)
        self.limpiar()
        self.nodos = datos["nodos"]
        self.aristas = datos["aristas"]
        for nombre, (x, y) in self.nodos.items():
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="lightblue", tags=nombre)
            self.canvas.create_text(x, y, text=nombre, tags=nombre)
        for origen in self.aristas:
            for destino, peso in self.aristas[origen].items():
                x1, y1 = self.nodos[origen]
                x2, y2 = self.nodos[destino]
                self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, tags=f"{origen}_{destino}")
                self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(peso), tags=f"{origen}_{destino}")
        messagebox.showinfo("Cargado", "Grafo cargado correctamente.")

    def exportar_imagen(self):
        G = nx.DiGraph()
        for origen in self.aristas:
            for destino, peso in self.aristas[origen].items():
                G.add_edge(origen, destino, weight=peso)
        pos = self.nodos
        nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=700, arrows=True)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.title("Exportación del grafo")
        archivo = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if archivo:
            plt.savefig(archivo)
            messagebox.showinfo("Exportado", f"Imagen guardada como '{archivo}'.")
            plt.close()
    def limpiar(self):
        self.canvas.delete("all")
        self.nodos.clear()
        self.aristas.clear()
        self.seleccion.clear()
        self.canvas.create_image(0, 0, image=self.imagen_fondo_tk, anchor="nw")

    def seleccionar_origen_destino(self, event):
        for nombre, (x, y) in self.nodos.items():
            if abs(event.x - x) < 20 and abs(event.y - y) < 20:
                if not self.origen_entry.get() or self.origen_entry.get() == "Nodo origen":
                    self.origen_entry.delete(0, tk.END)
                    self.origen_entry.insert(0, nombre)
                elif not self.destino_entry.get() or self.destino_entry.get() == "Nodo destino":
                    self.destino_entry.delete(0, tk.END)
                    self.destino_entry.insert(0, nombre)
                break

# Ejecutar la app
if __name__ == "__main__":
    root = tk.Tk()
    app = GPSApp(root)
    root.mainloop()