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
        frecuencia = combo_frecuencia.get()

        # Inicializamos los valores para el método de la secante
        i0 = 0.05  # Valor inicial 1
        i1 = 0.08  # Valor inicial 2

        # Calculamos la tasa de interés usando el método de la secante
        i_calculado = metodo_secante(V0, A, n, Vf, i0, i1)

        if i_calculado is None:
            messagebox.showerror("Error", "No se pudo encontrar la tasa de interés. Intenta con otros valores iniciales.")
            return

        # Ajuste de la cantidad de periodos dependiendo de la frecuencia de los aportes
        if frecuencia == 'Mensual':
            n = n * 4  # Suponemos que la cantidad de periodos es en meses, multiplicamos por 4 (para semanales)
            A = A * 4  # Convertir aportes semanales a mensuales
        elif frecuencia == 'Bimestral':
            n = n * 2  # Convertir de semanas a bimestres
            A = A * 2  # Convertir aportes semanales a bimestrales
        elif frecuencia == 'Trimestral':
            n = n * 4 / 3  # Convertir de semanas a trimestres
            A = A * 4 / 3  # Convertir aportes semanales a trimestrales

        # Calcular los resultados para cada periodo
        capital = V0  # Capital inicial (se mantiene igual)
        historial = []
        for t in range(1, n + 1):
            # Calculamos la ganancia en base al capital y la tasa de interés
            ganancia = capital * i_calculado
            total = capital + ganancia  # El total es capital + ganancia

            # Sumar el aporte al total, y usar el total como el nuevo capital para el siguiente periodo
            if t > 1:  # A partir del segundo periodo, sumamos el aporte
                capital = total + A
                aporte = A
            else:
                capital = total
                aporte = 0  # El aporte es 0 en la primera iteración

            # Guardamos los resultados en el historial
            historial.append((t, aporte, round(capital - ganancia , 2), round(ganancia, 2), round(capital, 2)))
        Interes = float(i_calculado) * n
        # Mostrar la tasa de interés calculada
        label_resultado.config(text=f"Tasa de interés calculada: {Interes:.6f}")
        # Mostrar el historial en una nueva ventana
        mostrar_historial(historial)

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores válidos.")

# Función para limpiar los valores introducidos
def limpiar_valores():
    # Limpiar todos los campos de entrada
    entry_V0.delete(0, tk.END)
    entry_A.delete(0, tk.END)
    entry_n.delete(0, tk.END)
    entry_Vf.delete(0, tk.END)
    # Restablecer el valor predeterminado del combobox
    combo_frecuencia.set("Semanal")
    # Borrar el texto del resultado
    label_resultado.config(text="Tasa de interés calculada: ")

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

    # Agregar un scrollbar a la ventana de historial
    scrollbar = ttk.Scrollbar(ventana_historial, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns', padx=5, pady=10)

    center_window(ventana_historial)

def center_window(window):
    """ Centra una ventana en la pantalla. """
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f"+{x}+{y}")

# Crear la ventana principal
root = tk.Tk()
root.title("Simulación de Interés")
center_window(root)

# Crear un marco principal
frame_principal = ttk.Frame(root, padding="10")
frame_principal.grid(row=0, column=0)

bold_font = ("Helvetica", 9, "bold")

# Etiquetas y campos de entrada
ttk.Label(frame_principal, text="Valor Inicial (V0):", font=bold_font).grid(row=0, column=0, sticky="w", pady=5)
entry_V0 = ttk.Entry(frame_principal)
entry_V0.grid(row=0, column=1, pady=5)

ttk.Label(frame_principal, text="Aporte Periódico (A):", font=bold_font).grid(row=1, column=0, sticky="w", pady=5)
entry_A = ttk.Entry(frame_principal)
entry_A.grid(row=1, column=1, pady=5)

ttk.Label(frame_principal, text="Número de Periodos (n):", font=bold_font).grid(row=2, column=0, sticky="w", pady=5)
entry_n = ttk.Entry(frame_principal)
entry_n.grid(row=2, column=1, pady=5)

ttk.Label(frame_principal, text="Valor Final (Vf):", font=bold_font).grid(row=3, column=0, sticky="w", pady=5)
entry_Vf = ttk.Entry(frame_principal)
entry_Vf.grid(row=3, column=1, pady=5)

ttk.Label(frame_principal, text="Frecuencia de Aportes:", font=bold_font).grid(row=4, column=0, sticky="w", pady=5)
combo_frecuencia = ttk.Combobox(frame_principal, values=["Semanal", "Mensual", "Bimestral", "Trimestral"])
combo_frecuencia.set("Semanal")  # Valor predeterminado
combo_frecuencia.grid(row=4, column=1, pady=5)

# Botones en la interfaz
ttk.Button(frame_principal, text="Iniciar Simulación", command=iniciar_simulacion).grid(row=5, column=0, pady=10, padx=5)
ttk.Button(frame_principal, text="Limpiar Valores", command=limpiar_valores).grid(row=5, column=1, pady=10, padx=5)

# Etiqueta para mostrar el resultado
label_resultado = ttk.Label(frame_principal, text="Tasa de interés calculada: ", font=bold_font)
label_resultado.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
