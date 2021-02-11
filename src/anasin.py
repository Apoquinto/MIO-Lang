from src.stack import *
# Definicion de la clase Anasin
class Anasin:
    # Propiedades inmutables para la salida de datos.
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR
    error = False
    # Inicio de datos claves para el analex.
    def __init__(self):    
        self.dirFile = ''
        self.countLine = 0
        # Inicia la pila, definida en la clase pila.py
        self.pila = Stack()

    # Setter para la direccion
    def setDirFile(self, dir):
        self.dirFile = dir

    # Inicia el Analizador sintactico
    def iniciarAnasin(self):
        # Cargar los datos del archivo a la stack
        try:
            simFile = open(self.dirFile)
            # Carga las filas
            for line in simFile:
                # Los mete al stack para comparar.
                self.pila.addToken(line.strip('\n'))
            simFile.close()
        except:
            print("Archivo irreconocible")
        self.pila.invert()
        # Inicio el proceso de recursion para comprobar resultados.
        if( self.PROG() == -1 ):
            print(self.error("Compilación fallida."))
        else:
            print(self.success("Compilación exitosa :D."))
        self.reset()

    # Detecta la sentencia PROG
    def PROG(self):
        self.sigLine()
        print("Iniciando compilación...")
        self.sigLine()
        if(self.pila.nextToken() == 'PROGRAMA'):
            self.sigLine()
            if('[id]' in self.pila.nextToken()):
                return 1
                if(self.pila.nextToken() == 'FINPROG'):
                    if(self.pila.isEmpty()):
                        return 1
                    else:
                        return -1
                else:
                    self.msgFallo("Falta o es incorrecto el final del programa 'FINPROG'")
                    return -1
            else:
                self.msgFallo("No hay identificador para el programa, favor de agregarlo después de la sentencia PROGRAMA.")
                return -1    
        else:
            self.msgFallo("Falta o es incorrecto el inicio del programa 'PROGRAMA'")
            return -1
    
    def SENTS(self):
        self.pila.nextToken()

    def SENT(self):
        pass

    def ELEM(self):
        pass

    def COMPARA(self):
        pass

    def msgFallo(self, razon):
        print(self.error("Error: ") + razon + self.warning(" [Linea " + str(self.countLine) + ']'))

    def resultado(self):
        return self.pila.isEmpty()

    # Este metodo devuelve un mensaje que le envies en color Verde.
    def success(self, msg):
        return self.OK + msg + self.RESET

    # Este metodo devuelve el mensaje que le envies en color Amarillo
    def warning(self, msg):
        return self.WARNING + msg + self.RESET

    # Este metodo devuelve el mensaje que le envies en color Rojo
    def error(self, msg):
        return self.FAIL + msg + self.RESET

    def sigLine(self):
        self.countLine += 1

    def reset(self):
        self.countLine = 0