class Stack:
    # Inicializacion de la clase.
    def __init__(self):
        self.items = []
        lineCounter = 0
    # Retorna un booleano en caso de que este vacia
    def isEmpty(self):
        return self.items == []
    # Devuelve el elemento en el tope de la pila
    def top(self):
        return self.items[len(self.items)-1]
    # Recupera el token en el tope de la pila y lo elimina de la pila
    def nextToken(self):
        if self.isEmpty():
            return False
        else:
            return self.items.pop()
    # Anexa un token al tope de la pila
    def addToken(self, token):
        self.items.append(token)
    # Devuelve el numero de elementos de la pila
    def size(self):
        return len(self.items)
    # Imprime la pila actual
    def show(self):
        print(self.items)
    # Invierte el tope de la pila
    def invert(self):
        self.items = self.items[::-1]