class Fraction():
    '''Defines a Fraction type that has an integer numerator and a non-zero integer denominator'''

    def __init__(self, num=0, denom=1):
        ''' Creates a new Fraction with numerator num and denominator denom'''
        self.numerator = num
        if denom != 0:
            self.denominator = denom
        else:
            raise ZeroDivisionError
    
    def __str__(self):
        """ returns the fraction """
        return (f"{self.numerator}/{self.denominator}")
    
    def __add__(self, other):
        """ defines the + operator"""
        product_num = self.numerator*other.denominator + other.numerator*self.denominator
        product_denom = self.denominator * other.denominator
        product = Fraction(product_num, product_denom)
        return product
    
    def __mul__(self, other):
        """ defines the * operator """
        prod_num = self.numerator*other.numerator
        prod_denom = self.denominator*other.denominator
        product = Fraction(prod_num, prod_denom)
        return product
    
    def __eq__(self, other):
        """Implement the '==' operator on Fractions"""
        float1 = self.numerator / self.denominator
        float2 = other.numerator / other.denominator
        return float1 == float2
    
    def __repr__(self):
        """represents the fraction"""
        return f"Fraction({self.numerator}, {self.denominator})"

def find_gcd(num1, num2):
    """ 
    Returns the Greatest Common Divisor (GCD) of num1 and num2. 
    Assumes num1 and num2 are positive integers. 
    """
    smaller = min(num1, num2)
    for i in range(smaller, 1, -1):
        if num1 % i == 0 and num2 % i == 0:
            return i
    return 1

class ReducedFraction(Fraction):                  
    '''A version of Fraction that always keeps itself in maximally reduced form'''

    def __init__(self, numerator, denominator=1):
        """ Initialiser, given both numerator and denominator """        
        super().__init__(numerator, denominator)  # use Fraction.__init__ 
        self.__reduce__()                         # next, reduce the numerator/denominator 

    def __reduce__(self):
        """ reduces the fraction """
        GCD = find_gcd(self.numerator, self.denominator)
        if GCD != 1:
            self.numerator = self.numerator // GCD
            self.denominator = self.denominator // GCD
        return Fraction(self.numerator, self.denominator)
    
    def __repr__(self):
        """ returns the reduced fraction """
        return f"ReducedFraction({self.numerator}, {self.denominator})"
    
    def __add__(self, other):
        """defines the add operator"""
        fraction_result = super().__add__(other)   # uses the __add__ method from Fraction
        ###TO DO:###
        # create an instance of ReducedFraction using the Fraction object from earlier.
        # HINT: use the numerator and denominator from the fraction_result to make the reduced_result 
        reduced_result = ReducedFraction(fraction_result.numerator, fraction_result.denominator)
        return reduced_result    
    
    def __mul__(self, other):
        """defines the multiply operator"""
        fraction_result = super().__mul__(other)
        reduced_result = ReducedFraction(fraction_result.numerator, fraction_result.denominator)
        return reduced_result


f = Fraction(1, 6)
r = ReducedFraction(2, 6)

class MixedNumber():
    """Creates a class that shows a number and a fraction"""
    
    def __init__(self, integer, fraction):
        """init"""
        self.fraction = ReducedFraction(fraction)
        self.integer = integer
        whole_num = self.numerator // self.denominator
        if whole_num != 0:
            self.integer += whole_num
            self.numerator -= whole_num * self.denominator
    
    def __repr__(self):
        """repr"""
        return f"MixedNumber({self.integer}, {self.fraction})"
    
mixed_num = MixedNumber(3, Fraction(4, 6))
print(mixed_num)