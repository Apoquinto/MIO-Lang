from src.analex import *

# Clase de MiCLI, es el centro de comandos de .MIO.
class PseudoCLI:

    # Propiedades inmutables para la CLI.
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR
    on = True
    
    # Inicializacion del objeto
    def __init__(self, dir):
        self.dir = dir
        self.analex = Analex()

    # Este metodo sirve para imprimir la parte inicial del CLI en consola
    # Se le puede agregar varias cosas extra como: 
    # mostrar el usuario
    # mostrar la direccion actual de MiCLI
    # etc, etc
    def printShell(self):
        print(self.WARNING + "[MIO]~" + self.RESET, end = ' ')

    # Este metodo imprime un mensaje que le envies en color Verde.
    def success(self, msg):
        print(self.OK + msg + self.RESET)

    # Este metodo imprime el mensaje que le envies en color Amarillo
    def warning(self, msg):
        print(self.WARNING + msg + self.RESET)

    # Este metodo imprime el mensaje que le envies en color Rojo
    def error(self, msg):
        print(self.FAIL + msg + self.RESET)
    def listener(self):
        # Este comando se encarga de imprimir la parte inicial del CLI
        self.printShell()

        # Recoge el input de la consola.
        arg = input()
        # Separa la instruccion en cada token que la conforma.
        instruction = arg.split()

        # En caso de no enviar ninguna instruccion, esperar instruccion. 
        if(len(instruction) == 0):
            pass
        elif(instruction[0] == 'analex'):
            # Guarda la parte del comando que corresponde al archivo a leer.            
            dir = instruction[1]
            # Inicia el proceso del analex
            self.executeAnalex( dir )
            # Inicia el proceso del anasin
            self.executeAnasin( dir )
        # Muesra en consola la direccion actual de MiCLI
        elif(instruction[0] == 'dir'):
            self.viewDirectory()
        # Termina el proceso de MiCLI
        elif(instruction[0] == '\q'):
            self.error("MIOff")
            self.on = False
        # Inicia el proceso del anasin
        elif(instruction[0] == '\h'):
            self.help()
        # Avisa al usuario que su comando no coincide con ninguno implementado en MiCLI
        else:
            self.error('Comando desconocido, puede usar \h para ver los comandos :D')

    # Despliega el menu de ayuda de MiCLI
    def help(self):
        self.success("Welcome to MIhelp:")
        print(self.OK + 'analex ' + self.WARNING + '[archivo]' + self.RESET + ' - Te permite compilar un archivo MIO.' )
        print(self.OK + 'dir' + self.RESET + ' - Te avisa de la direccion base de la MipseudoCLI.')
        print(self.OK + '\q' + self.RESET + ' - Cierra MIpseudoCLI.')

    # Ejecuta Analex.
    def executeAnalex(self, source):
        if(source[-4:] == '.mio' ):
            lexFile = open(source[:-4] + '.lex', 'w+')
            lexFile.close()
            self.success('Ejecutando Analex')
            self.analex.setDir(self.dir)
            self.analex.setSource(source)
            self.analex.readSourceCode()
        else:
            self.error('El archivo no es un .mio :c')

    # Ejecuta Anasin.
    def executeAnasin(self, source):
        pass

    # Muestra el directorio actual.
    def viewDirectory(self):
        print(self.dir)