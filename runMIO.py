import os
from src.pseudoCLI import * 

# Busqueda del directorio actual.
dir = os.getcwd()

# Inicializacion de MiCLI.
MipseudoCLI = PseudoCLI(dir)

# Inicio del ciclo infinito de la CLI hasta que se cierre.
while MipseudoCLI.on:
    # Listener es la funcio encargada de recibir los comandos de la terminal con las opciones reconocidas por MiCLI.
    MipseudoCLI.listener()