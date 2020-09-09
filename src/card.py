class Card:

    def __init__(self,name, colour, value):
        self._name = name
        self._colour = colour
        self._value = value

    @property
    def name(self):
        return self._name

    @property
    def colour(self):
        return self._colour

    @property
    def value(self):
        return self._value

    @value.setter 
    def value(self, a): 
         self._value = a
    
    def __repr__(self):
        return self._name