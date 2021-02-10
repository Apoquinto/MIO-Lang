from io import *
import re

# Definicion de la clase Analex
class Analex:
    # Inicio de datos claves para el analex.
    def __init__(self):    
        self.dir = ''
        self.source = ''
        self.sourceCode = []
        self.tokens = []
        self.IDcount = 0
        self.TXTcount = 0
        self.reserveds = ['PROGRAMA', 'FINPROG', 'SI', 'ENTONCES', 'SINO', 'FINSI', 'REPITE', 'VECES', 'FINREP', 'IMPRIME', 'LEE']
        self.relationals = ['>', '<', '==', '=']
        self.aritmetics = ['+', '-', '*', '/']
        self.ids = {}
        self.texts = {}
        self.numerics = []
        self.count = [0]
        self.error = False

    # Setter para la direccion
    def setDir(self, dir):
        self.dir = dir

    # Setter para el archivo de codigo fuente
    def setSource(self, source):
        self.source = source

    # Abre el documento, lo vuelve lineas y esas lineas las transforma en tokens.
    def readSourceCode(self):
        # Creacion de la direccion real del archivo
        dirFile = self.dir + '/' + self.source
        # Se inicia un bloque try por si el archivo no existe.
        try:
            # Abre el archivo
            mioFile = open(dirFile)
            # Lee el archivo por lineas de codigo.
            contadorLinea = 0
            for line in mioFile:
                contadorLinea += 1
                # Salta las lineas comentario.
                if line[0] != '#':
                    # Separa la linea de tokens separados por espacios.
                    self.tokens.append(self.tokenizar(line.strip('\n')))
                    print(self.tokenizar(line.strip('\n')))
                    print(line.split()) 
                    # Realiza la cuenta de los elementos de la linea
                    #self.count.append(len(line.split())
            # Se cierra el archivo base.
            mioFile.close()
            # Se inicia el proceso de la identificacion de tokens
            if( len(self.tokens) > 0 ):
                # En caso de querrer ver las lineas que conforman al codigo, puede descomentar la siguiente linea.
                # print(self.sourceCode)
                # En caso de querrer ver los tokens, puede descomentar la siguiente linea.
                # print(self.tokens)
                # Inicia el proceso de la escritura del archivo .lex
                self.writeLexFile()
                # Inicia el proceso de la escritura del archivo .sim
                self.writeSimFile()
                # Limpia los datos del archivo anterior
                self.restart()
            # Elimina la posibilidad de que el archivo este vacio
            else:
                print("El fichero se encuentra vacio.")
        # En caso de no existir, avisa al usuario
        except:
            print("No se pudo localizar el archivo.") 

    # Crea el archivo.lex
    def writeLexFile(self):
        # Crea la direccion en la que se escribira el archivo
        arc = self.dir + '/' + self.source[:-4] + '.lex'
        # Si quiere ver la direccion del archivo, puede descomentar la siguiente linea
        # print(arc)
        # Abre el archivo en la direccion antes dicha y lo configura para escritura.
        lexFile = open(arc, 'w+')
        # inicio a leer los lineas del archivo donde estan los tokens.
        contLine = 0
        for line in self.tokens:
            contLine += 1
            # Agarrra los tokens de la linea respectiva.
            for token in line:
                # Compruebo si se encuentra en las palabras de sintaxis.
                if self.isSyntax(token):
                    # Compruebo si es un operador aritmetico.
                    if( token in self.aritmetics ):
                        lexFile.write("[op_ar]" + '\n')
                    # En el caso contrario, sabemos que se trata de una palabra reservada.
                    else:
                        lexFile.write(token + '\n')
                # Comprueba si es numerico
                elif(self.isNumeric(token)):
                    lexFile.write("[val]\n")
                    # Guarda el valor del numerico junto con su valor en decimal.
                    self.numerics.append([token, self.octal_a_decimal(token)])
                elif(self.isID(token)):
                    key = '[id]ID' + str(self.IDcount)
                    lexFile.write(key + "\n")
                    self.IDcount += 1
                    self.ids[key] = token
                elif(self.isText(token)):
                    key = '[txt]TXT' + str(self.TXTcount)
                    lexFile.write(key + "\n")                    
                    self.TXTcount += 1
                    self.texts[key] = token
                else:
                    print("Error en la linea " + contLine + ", caracter invalido.")
        # Cierra el archivo .lex.
        lexFile.close()

    # Crea el archivo .sim 
    def writeSimFile(self):
        # Consigue la direccion del codigo fuente.
        arc = self.dir + '/' + self.source[:-4] + '.sim'
        simFile = open(arc, 'w+')
        simFile.write("IDS\n")
        # Saca los valores del diccionario y los escribe en el archivo.
        keys = self.ids.keys()
        for key in keys:
            simFile.write(self.ids[key] + ',\t' + key +'\n')
        simFile.write("\nTXT\n")
        # Saca los valores del diccionario y los escribe en el archivo.
        keys = self.texts.keys()
        for key in keys:
            simFile.write(self.texts[key] + ',\t' + key +'\n')
        # Agarra los valores de los numericos y los escribe en el archivo.
        simFile.write("\nVAL\n")
        for octal, decimal in self.numerics:
            simFile.write(str(octal) + ',\t' + str(decimal) +'\n')
        # cierra el archivo.
        simFile.close()

    # Recibe un string de elementos
    # Devuelve los tokens del string
    def tokenizar(self, line):
        # Bandera para reconocer si hay un '"'
        comillaActiva = False
        # Se le agrega un espacio para que automaticamente el algortimo guarde el ultimo token
        line += ' '
        # Este es el constructor de tokens, ira guardando los caracteres hasta que se considere 
        # que ya no es parte de un token
        tokenAux = ''
        # Aqui guardamos los tokens finales de la lista
        tokens = []
        # Obtenemos el tama;o de la linea
        tam = len(line)
        # recorremos caracter por caracter
        for i in range(tam):
            # En caso de que se reconozca que es un texto, se segira otra regla para encontrar el token.
            if comillaActiva:
                # Primero buscamos priorizar su final encontrando su pareja.
                if(line[i] == '"'):
                    tokenAux += line[i]
                    comillaActiva = False
                # Agregamos una excepcion por si al final no existe la pareja
                elif(tam == i + 1):
                    tokens.append(tokenAux)                
                # Por definicion, se debe guardar como token incluso los espacios dentro de las comillas
                # Por lo que literalmente guardamos todo en nuestro token temporal hasta que encontremos
                # La pareja, es decir, se cambie 
                else:
                    tokenAux += line[i]
            else:
                # Si no es ni espacio en blanco ni comilla, entonces se agrega al token actual.
                if line[i] != ' ' and line[i] != '"':
                    tokenAux += line[i]
                # En caso de iniciar una comilla[texto] activa una bandera.
                elif(line[i] == '"'):
                    tokenAux += line[i]
                    comillaActiva = True
                # Como ya sabemos que tiene que ser un espacio en blanco, agregamos el token actual 
                # a los tokens de la linea y reiniciamos el token actual
                else:
                    tokens.append(tokenAux)
                    tokenAux = ''
        return tokens
    
    # Esta funcion verifica si un token pertenece al conjunto de palabras del lenguaje.
    def isSyntax(self, token):
        return (token in self.reserveds or 
                token in self.aritmetics or 
                token in self.relationals)

    # Este metodo retorna si el token pertenece al tipo numerico octal.
    def isNumeric(self, token):  
        flag = re.fullmatch('[0-8]+', token)
        return flag

    # Determina si el token es un identificador
    def isID(self, token):
        flag = re.fullmatch('[a-zA-Z][a-zA-Z0-9]+', token)
        return flag

    # Determina si el token es un texto
    def isText(self, token):
        flag = re.fullmatch('"[a-zA-Z0-9\s]+"', token)
        return flag

    # retorna el valor decimal de un valor octal
    def octal_a_decimal(self, octal):
        decimal = 0
        posicion = 0
        # Invertir octal, porque debemos recorrerlo de derecha a izquierda
        # pero for in empieza de izquierda a derecha
        octal = octal[::-1]
        for digito in octal:
            valor_entero = int(digito)
            numero_elevado = int(8 ** posicion)
            equivalencia = int(numero_elevado * valor_entero)
            decimal += equivalencia
            posicion += 1
        return decimal

    # Devuelve los valores a su defecto
    def restart(self):
        self.sourceCode = []
        self.tokens = []
        self.ids.clear()
        self.IDcount = 0
        self.texts.clear()
        self.TXTcount = 0
        self.numerics = []