import tkinter as tk
from tkinter import messagebox

class AhorroConInteresCompuesto:
    def __init__(self, deposito_inicial, aporte_periodico, tasa_interes_anual, periodo_aporte):
        self.deposito_inicial = deposito_inicial
        self.aporte_periodico = aporte_periodico
        self.tasa_interes_anual = tasa_interes_anual
        self.periodo_aporte = periodo_aporte
        self.historial = []

    def calcular_interes_periodico(self):
        if self.periodo_aporte == "semanal":
            return self.tasa_interes_anual / 52
        elif self.periodo_aporte == "mensual":
            return self.tasa_interes_anual / 12
        elif self.periodo_aporte == "bimestral":
            return self.tasa_interes_anual / 6
        elif self.periodo_aporte == "trimestral":
            return self.tasa_interes_anual / 4
        else:
            raise ValueError("Período de aporte no válido")

    def calcular_historial(self, num_periodos):
        interes_periodico = self.calcular_interes_periodico()
        capital = self.deposito_inicial

        for periodo in range(1, num_periodos + 1):
            ganancia = capital * interes_periodico
            capital += ganancia + self.aporte_periodico
            self.historial.append((periodo, round(capital, 2), round(ganancia, 2)))

    def mostrar_historial(self):
        historial_texto = "Periodo\tCapital\tGanancia\n"
        for periodo, capital, ganancia in self.historial:
            historial_texto += f"{periodo}\t{capital}\t{ganancia}\n"
        return historial_texto

def iniciar_simulacion():
    try:
        deposito_inicial = float(entry_deposito.get())
        aporte_periodico = float(entry_aporte.get())
        tasa_interes_anual = float(entry_tasa.get())
        periodo_aporte = entry_periodo.get().lower()
        num_periodos = int(entry_periodos.get())

        simulacion = AhorroConInteresCompuesto(deposito_inicial, aporte_periodico, tasa_interes_anual, periodo_aporte)
        simulacion.calcular_historial(num_periodos)

        # Mostrar la segunda ventana con el historial de resultados
        mostrar_resultados(simulacion.mostrar_historial())

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese todos los valores correctamente.")

def mostrar_resultados(historial_texto):
    ventana_resultados = tk.Toplevel()
    ventana_resultados.title("Resultados de la Simulación")

    text_resultados = tk.Text(ventana_resultados, width=50, height=20)
    text_resultados.insert(tk.END, historial_texto)
    text_resultados.pack()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Simulador de Ahorro con Interés Compuesto")

# Etiquetas y campos de entrada
tk.Label(ventana, text="Depósito Inicial:").grid(row=0, column=0)
entry_deposito = tk.Entry(ventana)
entry_deposito.grid(row=0, column=1)

tk.Label(ventana, text="Aporte Periódico:").grid(row=1, column=0)
entry_aporte = tk.Entry(ventana)
entry_aporte.grid(row=1, column=1)

tk.Label(ventana, text="Tasa de Interés Anual:").grid(row=2, column=0)
entry_tasa = tk.Entry(ventana)
entry_tasa.grid(row=2, column=1)

tk.Label(ventana, text="Periodo de Aporte (semanal, mensual, bimestral, trimestral):").grid(row=3, column=0)
entry_periodo = tk.Entry(ventana)
entry_periodo.grid(row=3, column=1)

tk.Label(ventana, text="Número de Periodos:").grid(row=4, column=0)
entry_periodos = tk.Entry(ventana)
entry_periodos.grid(row=4, column=1)

# Botón para iniciar la simulación
boton_simular = tk.Button(ventana, text="Iniciar Simulación", command=iniciar_simulacion)
boton_simular.grid(row=5, column=0, columnspan=2)

ventana.mainloop()

