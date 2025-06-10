"""
Calcular el area de un triangulo
donde:
    b = base
    h = altura
ecuacion:
    (b*h)/2
"""
def area(b, h):
    if b <= 0:
        raise ValueError("La base debe ser mayor que cero")
    if h <= 0:
        raise ValueError("La altura debe ser mayor que cero")
    
    ec = (b * h) / 2
    return ec