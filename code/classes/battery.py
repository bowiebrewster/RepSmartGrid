class Battery():
    
    colors = ['#0fa2a9', '#ff1463', '#b479bb', '#15362f', '#68da23']

    def __init__(self, number, x, y, capacity):
        self.number = number
        self.x = x
        self.y = y
        self.capacity = capacity
        self.color = Battery.colors[self.number - 1]
        self.is_full = False

    def is_feasible(self, house):
        """
        Returns true if battery can take given house and subtract house output from battery capacity.
        """
        if house.output > self.capacity:
            return False
        self.capacity -= house.output
        return True

    def __str__(self):
        return f'{self.number}'