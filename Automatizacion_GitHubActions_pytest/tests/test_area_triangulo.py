from calc_area import area
import pytest

def primer_test():
    """Validar el resultado cuando la base sea 5 y la altura sea 7"""
    assert area(5, 7) == pytest.approx(17.5)

def test_no_negativos_base():
    """Validar que no se acepten valores negativos para la base"""
    with pytest.raises(ValueError, match="La base debe ser mayor que cero"):
        area(-5, 7)

def test_no_negativos_altura():
    """Validar que no se acepten valores negativos para la altura"""
    with pytest.raises(ValueError, match="La altura debe ser mayor que cero"):
        area(5, -7)

def test_no_negativos_ambos():
    """Validar que no se acepten valores negativos para ambos parámetros"""
    with pytest.raises(ValueError):
        area(-5, -7)

def test_base_no_cero():
    """Validar que la base no sea cero"""
    with pytest.raises(ValueError, match="La base debe ser mayor que cero"):
        area(0, 7)

def test_altura_no_cero():
    """Validar que la altura no sea cero"""
    with pytest.raises(ValueError, match="La altura debe ser mayor que cero"):
        area(5, 0)

def test_valores_positivos_validos():
    """Test adicional: Validar cálculo con otros valores positivos"""
    assert area(10, 4) == pytest.approx(20.0)
    assert area(3, 6) == pytest.approx(9.0)