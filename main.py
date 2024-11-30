import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Función que representa la ecuación a resolver
def calcular_ecuacion(i, V0, A, n, Vf):
    """
    Calcula el valor de la función financiera con base en la tasa de interés (i)
    y los parámetros ingresados.
    """
    return V0 * (1 + i)**n + A * ((1 + i)**n - (1 + i)) / i - Vf

# Método de la secante
def metodo_secante(V0, A, n, Vf, interes_inicial_1, interes_inicial_2, tol=1e-10, max_iter=100):
    """
    Resuelve una ecuación no lineal mediante el método de la secante.
    """
    iteraciones = 0
    while iteraciones < max_iter:
        f_i0 = calcular_ecuacion(interes_inicial_1, V0, A, n, Vf)
        f_i1 = calcular_ecuacion(interes_inicial_2, V0, A, n, Vf)

        if abs(f_i1 - f_i0) < tol:
            return None  # Evitar división por cero

        nuevo_interes = interes_inicial_2 - f_i1 * (interes_inicial_2 - interes_inicial_1) / (f_i1 - f_i0)

        if abs(nuevo_interes - interes_inicial_2) < tol:
            return nuevo_interes  # Converge

        interes_inicial_1, interes_inicial_2 = interes_inicial_2, nuevo_interes
        iteraciones += 1

    return None

# Ajustar frecuencia de aportes
def ajustar_frecuencia(frecuencia, n, A):
    """
    Ajusta el número de periodos y el aporte periódico según la frecuencia seleccionada.
    """
    if frecuencia == 'Mensual':
        n, A = n * 4, A * 4
    elif frecuencia == 'Bimestral':
        n, A = n * 2, A * 2
    elif frecuencia == 'Trimestral':
        n, A = n * 4 / 3, A * 4 / 3
    return int(n), A

# Inicia la simulación
def iniciar_simulacion():
    try:
        V0 = float(entry_V0.get())
        A = float(entry_A.get())
        n = int(entry_n.get())
        Vf = float(entry_Vf.get())
        frecuencia = combo_frecuencia.get()

        i0, i1 = 0.05, 0.08
        i_calculado = metodo_secante(V0, A, n, Vf, i0, i1)

        if i_calculado is None:
            messagebox.showerror("Error", "No se pudo encontrar la tasa de interés. Intenta con otros valores iniciales.")
            return

        n, A = ajustar_frecuencia(frecuencia, n, A)

        # Cálculo de resultados
        capital = V0
        historial = []
        for t in range(1, n + 1):
            ganancia = capital * i_calculado
            total = capital + ganancia
            aporte = A if t > 1 else 0
            capital = total + aporte
            historial.append((t, aporte, round(capital - ganancia, 2), round(ganancia, 2), round(capital, 2)))

        Interes = float(i_calculado) * n
        label_resultado.config(text=f"Tasa de interés calculada: {Interes:.6f}")
        mostrar_historial(historial)

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores válidos.")

# Función para mostrar el historial en una nueva ventana
def mostrar_historial(historial):
    """
    Crea una ventana emergente para mostrar el historial de resultados en formato tabular.
    """
    ventana_historial = tk.Toplevel(root)
    ventana_historial.title("Historial de Resultados")

    tree = ttk.Treeview(ventana_historial, columns=("Periodo", "Aporte", "Capital", "Ganancia", "Total"), show="headings")
    tree.heading("Periodo", text="Periodo")
    tree.heading("Aporte", text="Aporte")
    tree.heading("Capital", text="Capital")
    tree.heading("Ganancia", text="Ganancia")
    tree.heading("Total", text="Total")
    tree.grid(row=0, column=0, pady=10, padx=10)

    for row in historial:
        tree.insert("", "end", values=row)

    scrollbar = ttk.Scrollbar(ventana_historial, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns', padx=5, pady=10)

    center_window(ventana_historial)

# Centra una ventana en la pantalla
def center_window(window):
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

# Botón para iniciar la simulación
ttk.Button(frame_principal, text="Iniciar Simulación", command=iniciar_simulacion).grid(row=5, column=0, columnspan=2, pady=10)

# Etiqueta para mostrar el resultado
label_resultado = ttk.Label(frame_principal, text="Tasa de interés calculada: ")
label_resultado.grid(row=6, column=0, columnspan=2, pady=5)

# Iniciar la aplicación
root.mainloop()
