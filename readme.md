# PROYECTO BIMESTRAL - MÉTODOS NUMÉRICOS

# BELEN RAURA
# ANDRES FERNANDEZ
# DAVID PUGA
# KENNET YAR

# Descripción
Un prestigioso banco lo ha contratado para implementar la calculadora de un programa de ahorro moderno. 
Este programa consiste de:
* Un depósito inicial de al menos 50 dólares y
* aportes semanales de al menos 5 dólares.

Los técnicos del banco le han proporcionado la fórmula básica para calcular el interés compuesto:

$V_f=V_o(1+i)^n$
Donde:
* $V_f$ es el valor final en la cuenta de ahorros,
* $V_o$ es el valor de depósito inicial,
* $i$ es la tasa de interés,
* $n$ es el número de periodos transcuridos.


Sin embargo, esta fórmula **ESTÁ INCOMPLETA**, pues los técnicos del banco desconocen cómo se debe calcular los interes en base a los aportes semanales. Parte de su proyecto es establecer la expresión matemática para encontrar la tasa de interés. 

En su lugar le han dado el siguiente ejemplo:

## Ejemplo
Dado un depósito inicial de 100 dólares, aportes semanales de 5 dólares y una tasa de interés anual del 8%, la tabla de cálculo sería la siguiente:

|  Semana  |  Aporte ($)  |  Capital ($)  |  Ganancia ($)  |  Total ($)  |
|  ---     |         ---  |          ---  |           ---  |        ---  |
|  1  |  100 |   100        |   0.15    |   100.15  |
|  2  |  5   |   105.15     |   0.16    |   105.31  |
|  3  |  5   |   110.31     |   0.17    |   110.48  |
|  4  |  5   |   115.48     |   0.18    |   115.66  |
|  5  |  5   |   120.66     |   0.19    |   120.85  |
...
|  51  |  5  |   367.65     |   0.57    |   368.22  |
|  52  |  5  |   373.22     |   0.57    |   373.79  |


# Objetivo
Los técnicos del banco desean la calculadora para probar diferentes escenarios de ahorro, con el objetivo principal de determinar la tasa de **interés**. 

* Considere que el banco puede cambiar de opinión y pedirle que los aportes ya no sean semanales, sino mensuales, trimestrales o bimestrales. Incluya esta posibilidad en su programa.