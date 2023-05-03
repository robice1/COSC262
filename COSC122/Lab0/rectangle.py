class Rectangle(object):
    """ Rectangle class """
    def __init__(self, width=1, height=2):
        self.width = width
        self.height = height
    
    def area(self):
        """ Returns area """
        return self.width * self.height
    
    def perimeter(self):
        """ Returns perimeter """
        return (2 * self.width + 2 * self.height)
    
    def __str__(self):
        """ returns rectangle drawn in # """
        line = '#' * self.width
        box = (line + '\n') * self.height
        return box
        
    
recker = Rectangle(3, 2)
print(recker)
recker = Rectangle(2, 3)
print(recker)
recker = Rectangle(20, 5)
print(recker)