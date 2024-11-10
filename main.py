class AhorroConInteresCompuesto:
    def __init__(self, deposito_inicial, aporte_periodico, tasa_interes_anual, periodo_aporte):
        """
        Inicializa el programa de ahorro.
        
        - deposito_inicial: Capital inicial en la cuenta.
        - aporte_periodico: Monto de cada aporte periódico.
        - tasa_interes_anual: Tasa de interés anual (en decimal, e.g., 0.08 para 8%).
        - periodo_aporte: Periodo de aporte ("semanal", "mensual", "bimestral", "trimestral").
        """
        self.deposito_inicial = deposito_inicial
        self.aporte_periodico = aporte_periodico
        self.tasa_interes_anual = tasa_interes_anual
        self.periodo_aporte = periodo_aporte
        self.interes_periodico = self.calcula_interes_periodico()
        self.balance = deposito_inicial

    def calcula_interes_periodico(self):
        """
        Calcula la tasa de interés efectiva según el periodo de aporte.
        """
        if self.periodo_aporte == "semanal":
            return self.tasa_interes_anual / 52
        elif self.periodo_aporte == "mensual":
            return self.tasa_interes_anual / 12
        elif self.periodo_aporte == "bimestral":
            return self.tasa_interes_anual / 6
        elif self.periodo_aporte == "trimestral":
            return self.tasa_interes_anual / 4
        else:
            raise ValueError("Periodo de aporte no válido.")

    def simular_ahorro(self, num_periodos):
        """
        Simula el crecimiento del ahorro durante un número de periodos.

        - num_periodos: Número total de periodos para la simulación.
        """
        historial = []
        balance = self.deposito_inicial
        
        for periodo in range(1, num_periodos + 1):
            # Se aplica el interés compuesto
            ganancia_interes = balance * self.interes_periodico
            balance += ganancia_interes + self.aporte_periodico

            # Guardar el estado actual en el historial
            historial.append({
                "Periodo": periodo,
                "Aporte": self.aporte_periodico,
                "Capital": round(balance - ganancia_interes, 2),
                "Ganancia": round(ganancia_interes, 2),
                "Total": round(balance, 2)
            })

        return historial

    def mostrar_historial(self, num_periodos):
        """
        Muestra el historial de la simulación.
        """
        historial = self.simular_ahorro(num_periodos)
        print("Periodo\tAporte\tCapital\tGanancia\tTotal")
        for registro in historial:
            print(f"{registro['Periodo']}\t{registro['Aporte']}\t{registro['Capital']}\t{registro['Ganancia']}\t{registro['Total']}")


# Parámetros de ejemplo
deposito_inicial = 100  # Depósito inicial de 100 unidades
aporte_periodico = 5    # Aporte periódico de 5 unidades
tasa_interes_anual = 0.08  # Tasa de interés anual del 8%
periodo_aporte = "semanal"  # Aportes semanales
num_periodos = 52  # Número de periodos para un año (52 semanas)

# Crear y ejecutar la simulación
simulacion = AhorroConInteresCompuesto(deposito_inicial, aporte_periodico, tasa_interes_anual, periodo_aporte)
simulacion.mostrar_historial(num_periodos)
