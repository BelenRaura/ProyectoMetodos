import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Función que representa la ecuación a resolver
def f(i, V0, A, n, Vf):
    return V0 * (1 + i)**n + A * ((1 + i)**n - (1 + i)) / i - Vf

# Método de la secante
def metodo_secante(V0, A, n, Vf, i0, i1, tol=1e-10, max_iter=100):
    iteraciones = 0
    while iteraciones < max_iter:
        # Calculamos los valores de la función en i0 y i1
        f_i0 = f(i0, V0, A, n, Vf)
        f_i1 = f(i1, V0, A, n, Vf)

        # Comprobamos si la diferencia entre las funciones es pequeña para evitar división por 0
        if abs(f_i1 - f_i0) < tol:
            return None

        # Calculamos el nuevo valor de i usando la fórmula del método de la secante
        i_next = i1 - f_i1 * (i1 - i0) / (f_i1 - f_i0)

        # Comprobamos si la diferencia entre i_next y i1 es suficientemente pequeña
        if abs(i_next - i1) < tol:
            return i_next

        # Actualizamos i0 e i1 para la siguiente iteración
        i0, i1 = i1, i_next
        iteraciones += 1

    return None

# Función que se ejecuta cuando el usuario presiona el botón
def iniciar_simulacion():
    try:
        # Obtenemos los valores introducidos por el usuario
        V0 = float(entry_V0.get())
        A = float(entry_A.get())
        n = int(entry_n.get())
        Vf = float(entry_Vf.get())

        # Inicializamos los valores para el método de la secante
        i0 = 0.05  # Valor inicial 1
        i1 = 0.06  # Valor inicial 2

        # Calculamos la tasa de interés usando el método de la secante
        i_calculado = metodo_secante(V0, A, n, Vf, i0, i1)

        if i_calculado is None:
            messagebox.showerror("Error", "No se pudo encontrar la tasa de interés. Intenta con otros valores iniciales.")
            return

        # Mostrar la tasa de interés calculada
        label_resultado.config(text=f"Tasa de interés calculada: {i_calculado:.6f}")

        # Calcular los resultados para cada periodo
        total = V0  # Capital inicial
        historial = []
        for t in range(1, n + 1):
            # Cálculo de la ganancia y el total por periodo
            ganancia = A * ((1 + i_calculado)**t - 1) / i_calculado
            total += ganancia
            capital = V0 * (1 + i_calculado)**t
            # Guardamos los resultados en el historial
            historial.append((t, A, round(capital, 2), round(ganancia, 2), round(total, 2)))

        # Mostrar el historial en una nueva ventana
        mostrar_historial(historial)

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores válidos.")

# Función para mostrar el historial en una nueva ventana
def mostrar_historial(historial):
    # Crear una nueva ventana
    ventana_historial = tk.Toplevel(root)
    ventana_historial.title("Historial de Resultados")

    # Crear la tabla para mostrar los resultados en la nueva ventana
    tree = ttk.Treeview(ventana_historial, columns=("Periodo", "Aporte", "Capital", "Ganancia", "Total"), show="headings")
    tree.heading("Periodo", text="Periodo")
    tree.heading("Aporte", text="Aporte")
    tree.heading("Capital", text="Capital")
    tree.heading("Ganancia", text="Ganancia")
    tree.heading("Total", text="Total")
    tree.grid(row=0, column=0, pady=10, padx=10)

    # Insertar los resultados en la tabla
    for row in historial:
        tree.insert("", "end", values=row)

# Crear la ventana principal
root = tk.Tk()
root.title("Simulación de Interés")

# Crear un marco principal
frame_principal = ttk.Frame(root, padding="10")
frame_principal.grid(row=0, column=0)

# Etiquetas y campos de entrada
ttk.Label(frame_principal, text="Valor Inicial (V0):").grid(row=0, column=0, sticky="w", pady=5)
entry_V0 = ttk.Entry(frame_principal)
entry_V0.grid(row=0, column=1, pady=5)

ttk.Label(frame_principal, text="Aporte Periódico (A):").grid(row=1, column=0, sticky="w", pady=5)
entry_A = ttk.Entry(frame_principal)
entry_A.grid(row=1, column=1, pady=5)

ttk.Label(frame_principal, text="Número de Periodos (n):").grid(row=2, column=0, sticky="w", pady=5)
entry_n = ttk.Entry(frame_principal)
entry_n.grid(row=2, column=1, pady=5)

ttk.Label(frame_principal, text="Valor Final (Vf):").grid(row=3, column=0, sticky="w", pady=5)
entry_Vf = ttk.Entry(frame_principal)
entry_Vf.grid(row=3, column=1, pady=5)

# Botón para iniciar la simulación
ttk.Button(frame_principal, text="Iniciar Simulación", command=iniciar_simulacion).grid(row=4, column=0, columnspan=2, pady=10)

# Etiqueta para mostrar el resultado
label_resultado = ttk.Label(frame_principal, text="Tasa de interés calculada: ")
label_resultado.grid(row=5, column=0, columnspan=2, pady=5)

# Iniciar la aplicación
root.mainloop()
