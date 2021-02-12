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
        self.countLine = 1
        # Inicia la pila, definida en la clase pila.py
        self.pila = Stack()
        self.works = True

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
        self.PROG()
        if( self.works ):
            print(self.success("Compilación exitosa :D."))
        else:
            print(self.error("Compilación fallida."))
        self.reset()

    # Detecta la sentencia PROG
    def PROG(self):
        print("Iniciando compilación...")
        # VErifica que el prograa este iniciado
        if(self.pila.nextToken() == 'PROGRAMA'):
            self.sigLine()
            # Busca el identificador del programa
            if('[id]' in self.pila.nextToken()):
                # Inicia el reconocimiento de sentencia
                self.SENTS()
                # Por ultimo, realiza la comprobacion de finalizacion
                if(self.pila.nextToken() == 'FINPROG'):
                    if(self.pila.isEmpty()):
                        pass
                    else:
                        self.msgFallo("Quedan elementos despues del FINPROG")
                else:
                    self.msgFallo("Falta o es incorrecto el final del programa 'FINPROG'")
            else:
                self.msgFallo("No hay identificador para el programa, favor de agregarlo después de la sentencia PROGRAMA.")
        else:
            self.msgFallo("Falta o es incorrecto el inicio del programa 'PROGRAMA'")
    
    def SENTS(self):
        # Guardo el elemento actual de la pila para comparar.
        token = self.pila.top()
        # Compruebo que sea el FINPROGRAM para finalizar la recusion
        # En un principio iba usarlo de return, pero asi se dificultaba validar el mensaje del FINPROG faltante
        if( token == 'FINPROG' or token == 'FINREP' or token == 'FINSI' ):
            pass
        # Compruebo si es una sentencia valida
        elif('[id]' in token or token in ['SI', 'IMPRIME', 'REPITE', 'LEE']):
            self.SENT()
            self.SENTS()
        # En cualquier otro caso, mando mensaje de error.
        else:
            self.pila.nextToken()
            self.msgFallo("La sentencia no tiene sentido (pendiente redactar un mensaje mas informativo).")

    def SENT(self):
        # Saco el siguiente elemento de la pila
        self.sigLine()
        token = self.pila.nextToken()
        # Sentencia [ID]
        if('[id]' in token):
            self.sigLine()
            token = self.pila.nextToken()
            if(token == '='):
                self.sigLine()
                if(self.ELEM()):
                    self.pila.nextToken()
                    if(self.pila.nextToken() == '[op_ar]'):
                        if(self.ELEM()):
                            self.sigLine()
                            self.pila.nextToken()
                        else:                            
                            self.msgFallo("Después de un operador aritmetico debe ir un valor o un identificador.")
                else:
                    self.sigLine()
                    self.pila.nextToken()
                    self.msgFallo("Para la asignación se debe tratar de un valor o un identificador.")
            else:
                self.msgFallo("Falta el signo de asignación para el [id]")
        # Sentencia LEE
        if(token == 'LEE'):
            self.sigLine()
            if('[id]' not in self.pila.nextToken()):
                self.msgFallo("La instruccion LEE debe estar seguida de un identificador.")
        # Sentencia IMPRIME
        if(token == 'IMPRIME'):
            self.sigLine()
            # Compruebo si no es ni un texto y llamo a ELEM a ver si es un ELEM.
            if('[txt]' not in self.pila.top() and not self.ELEM()):
                self.msgFallo("La instruccion IMPRIME debe estar seguida de un texto, un identificador o un valor.")
            # Elimino el token actual.
            self.pila.nextToken()
        # Sentencia REPITE
        if(token == 'REPITE'):
            self.sigLine()
            if(self.ELEM()):
                self.sigLine()
                self.pila.nextToken()
                if(self.pila.nextToken() == "VECES"):
                    self.SENTS()
                    if(self.pila.top()=='FINREP'):
                        self.sigLine()
                        self.pila.nextToken()
                    else:
                        self.msgFallo("REPITE VECES no finalizado, favor de poner un FINREP.")
                else:
                    self.msgFallo("Después de indicar un valor o un identificador se debe de poner la palabra reservada 'VECES'")
            else:
                self.sigLine()
                self.pila.nextToken()
                self.msgFallo("Después de REPITE favor de colocar un valor o un identificador")
        # Sentencia S.
        if(token == 'SI'):
            self.sigLine()
            self.COMPARA()
            if(self.pila.nextToken() == "ENTONCES"):
                self.SENTS()
                if(self.pila.top()=='FINSI'):
                    self.sigLine()
                    self.pila.nextToken()
                else:
                    self.msgFallo("SI no finalizado, favor de poner un FINSI.")
            else:
                self.msgFallo("Después de indicar un valor o un identificador se debe de poner la palabra reservada 'ENTONCES'")
            
    def ELEM(self):
        if( '[id]' in self.pila.top() or '[val]' in self.pila.top() ):
            return True
        else:
            return False

    def COMPARA(self):
        self.sigLine()
        if('[id]' in self.pila.nextToken()):
            self.sigLine()
            if('[op_rel]' in self.pila.nextToken()):
                if(self.ELEM()):
                    self.sigLine()
                    self.pila.nextToken()
                else:
                    self.sigLine()
                    self.msgFallo("El comparador requiere un vakor o un identificador despues de la comparación.")
            else:
                self.msgFallo("Falta el operador relacional.")
        else:
            self.msgFallo("Para comparar se tiene que usar necesariamente un identificador inicial.")

    def msgFallo(self, razon):
        print(self.error("Error: ") + razon + self.warning(" [Linea " + str(self.countLine) + ']'))
        self.works = False

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
        self.countLine = 1
        self.pila = Stack()
        self.works = True