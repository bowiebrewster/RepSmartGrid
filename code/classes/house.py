class House():
    def __init__(self, number, x, y, output):
        self.number = number
        self.x = x
        self.y = y
        self.output = output
        self.is_available = True

    def __str__(self):
        return f'{self.number}'