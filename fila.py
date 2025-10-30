class Fila:
    def __init__(self):
        self.items = []

    def esta_vazia(self):
        return not self.items

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.esta_vazia():
            return self.items.pop(0)
        return None

    def tamanho(self):
        return len(self.items)