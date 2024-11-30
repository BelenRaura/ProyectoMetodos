import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

class AhorroConInteresCompuesto:
    def __init__(self, deposito_inicial, aporte_periodico, tasa_interes_anual, periodo_aporte):
        self.deposito_inicial = deposito_inicial
        self.aporte_periodico = aporte_periodico
        self.tasa_interes_anual = tasa_interes_anual
        self.periodo_aporte = periodo_aporte
        self.historial = []

    def calcular_interes_periodico(self):
        periodos = {"Semanal": 52, "Mensual": 12, "Bimestral": 6, "Trimestral": 4}
        if self.periodo_aporte not in periodos:
            raise ValueError(f"Período de aporte '{self.periodo_aporte}' no válido.")
        return self.tasa_interes_anual / periodos[self.periodo_aporte]/100


    def calcular_historial(self, num_periodos):
        interes_periodico = self.calcular_interes_periodico()
        capital = self.deposito_inicial
        self.historial = []

        for periodo in range(1, num_periodos + 1):
            if periodo == 1:
                ganancia = capital * interes_periodico
                total = capital + ganancia
                self.historial.append((periodo, round(self.deposito_inicial, 2), round(capital, 2), round(ganancia, 2), round(total, 2)))
            else:
                capital += self.aporte_periodico + ganancia
                ganancia = capital * interes_periodico
                total = capital + ganancia 
                self.historial.append((periodo, round(self.aporte_periodico, 2), round(capital, 2), round(ganancia, 2), round(total, 2)))
def validar_entradas():
    """Verifica que todas las entradas sean válidas antes de proceder."""
    if not entry_deposito.get().strip() or not entry_aporte.get().strip() or not entry_tasa.get().strip() or not entry_periodos.get().strip():
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return False
    try:
        deposito_inicial = float(entry_deposito.get())
        aporte_periodico = float(entry_aporte.get())
        tasa_interes_anual = float(entry_tasa.get())
        periodo_aporte = combo_periodo.get().strip()
        num_periodos = int(entry_periodos.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")
        return False
    if tasa_interes_anual < 0:
        messagebox.showerror("Error", "La tasa de interés no puede ser negativa.")
        return False
    if deposito_inicial < 50:
        messagebox.showerror("Error", "El depósito inicial debe ser de al menos 50 dólares")
        return False
    if aporte_periodico < 5:
        messagebox.showerror("Error", "Los aportes periódicos deben ser de al menos 5 dólares por cada periodo")
        return False
    if num_periodos <= 0:
        messagebox.showerror("Error", "Número invalido de periodos")
        return False
    if combo_periodo.get() not in ["Semanal", "Mensual", "Bimestral", "Trimestral"]:
        messagebox.showerror("Error", "Seleccione un período de aporte válido.")
        return False
    return True

def iniciar_simulacion():
    if not validar_entradas():
        return

    try:
        deposito_inicial = float(entry_deposito.get())
        aporte_periodico = float(entry_aporte.get())
        tasa_interes_anual = float(entry_tasa.get())
        periodo_aporte = combo_periodo.get().strip()
        num_periodos = int(entry_periodos.get())

        simulacion = AhorroConInteresCompuesto(deposito_inicial, aporte_periodico, tasa_interes_anual, periodo_aporte)
        simulacion.calcular_historial(num_periodos)

        mostrar_resultados(simulacion.historial)
    except Exception as e:
        messagebox.showerror("Error inesperado", f"{str(e)}")

def mostrar_resultados(historial):
    ventana_resultados = ttk.Toplevel()
    ventana_resultados.title("Resultados de la Simulación")
    ventana_resultados.geometry("800x400")
    ventana_resultados.resizable(False,False)

    frame_resultados = ttk.Frame(ventana_resultados, padding=10)
    frame_resultados.pack(fill=BOTH, expand=True)

    style = ttk.Style()
    style.configure("Treeview.Heading", background="#127FA4", foreground="white", font=("Helvetica", 10, "bold"))

    tree = ttk.Treeview(
        frame_resultados,
        columns=("Periodo", "Aporte ($)", "Capital ($)", "Ganancia ($)", "Total ($)"),
        show="headings"
    )
    
    tree.heading("Periodo", text="Periodo")
    tree.heading("Aporte ($)", text="Aporte ($)")
    tree.heading("Capital ($)", text="Capital ($)")
    tree.heading("Ganancia ($)", text="Ganancia ($)")
    tree.heading("Total ($)", text="Total ($)")

    tree.column("Periodo", anchor=CENTER, width=100)
    tree.column("Aporte ($)", anchor=CENTER, width=150)
    tree.column("Capital ($)", anchor=CENTER, width=150)
    tree.column("Ganancia ($)", anchor=CENTER, width=150)
    tree.column("Total ($)", anchor=CENTER, width=150)

    for fila in historial:
        tree.insert("", END, values=fila)

    scrollbar = ttk.Scrollbar(frame_resultados, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    frame_resultados.columnconfigure(0, weight=1)
    frame_resultados.rowconfigure(0, weight=1)

    def cerrar_ventana():
        tree.configure(yscrollcommand=None)
        ventana_resultados.destroy()

    ventana_resultados.protocol("WM_DELETE_WINDOW", cerrar_ventana)

    boton_cerrar = ttk.Button(frame_resultados, text="Cerrar", bootstyle=DANGER, command=cerrar_ventana)
    boton_cerrar.grid(row=1, column=0, columnspan=2, pady=10)

def limpiar_campos():
    entry_deposito.delete(0, END)
    entry_aporte.delete(0, END)
    entry_tasa.delete(0, END)
    combo_periodo.set("")
    entry_periodos.delete(0, END)

# Crear la ventana principal
ventana = ttk.Window(themename="superhero")
ventana.title("Simulador de Ahorro con Interés Compuesto")
ventana.geometry("500x400")
ventana.resizable(False, False)

# Encabezado
ttk.Label(ventana, text="Simulador de Ahorro", font=("Helvetica", 20, "bold"), bootstyle=PRIMARY).pack(pady=10)

frame_principal = ttk.Frame(ventana, padding=10)
frame_principal.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Entrada de datos
ttk.Label(frame_principal, text="Depósito Inicial:", bootstyle="info").grid(row=0, column=0, sticky="W", pady=5)
entry_deposito = ttk.Entry(frame_principal, bootstyle=INFO)
entry_deposito.grid(row=0, column=1, pady=5)

ttk.Label(frame_principal, text="Aporte Periódico:", bootstyle="info").grid(row=1, column=0, sticky="W", pady=5)
entry_aporte = ttk.Entry(frame_principal, bootstyle=INFO)
entry_aporte.grid(row=1, column=1, pady=5)

ttk.Label(frame_principal, text="Tasa de Interés Anual (%):", bootstyle="info").grid(row=2, column=0, sticky="W", pady=5)
entry_tasa = ttk.Entry(frame_principal, bootstyle=INFO)
entry_tasa.grid(row=2, column=1, pady=5)

ttk.Label(frame_principal, text="Periodo de Aporte:", bootstyle="info").grid(row=3, column=0, sticky="W", pady=5)
combo_periodo = ttk.Combobox(frame_principal, values=["Semanal", "Mensual", "Bimestral", "Trimestral"], state="readonly")
combo_periodo.grid(row=3, column=1, pady=5)

ttk.Label(frame_principal, text="Número de Periodos:", bootstyle="info").grid(row=4, column=0, sticky="W", pady=5)
entry_periodos = ttk.Entry(frame_principal, bootstyle=INFO)
entry_periodos.grid(row=4, column=1, pady=5)

# Botones
ttk.Button(frame_principal, text="Iniciar Simulación", bootstyle=SUCCESS, command=iniciar_simulacion).grid(row=5, column=0, columnspan=1, pady=10)
ttk.Button(frame_principal, text="Limpiar", bootstyle=WARNING, command=limpiar_campos).grid(row=5, column=1, columnspan=1, pady=10)

ventana.mainloop()