"""
Utilidades para el sistema SISFAC
"""

def numero_a_texto(numero):
    """
    Convierte un número a su representación en texto en español.
    
    Ejemplos:
        1234.56 -> "Mil doscientos treinta y cuatro con 56/100"
        100.00 -> "Cien con 00/100"
        0.50 -> "Cero con 50/100"
    """
    # Convertir a float para manejar decimales
    numero_float = float(numero)
    
    if numero_float == 0:
        return "Cero con 00/100"
    
    # Separar parte entera y decimal
    entero = int(numero_float)
    decimal = int(round((numero_float - entero) * 100))
    
    # Convertir parte entera a texto
    texto_entero = convertir_entero(entero)
    
    # Formatear decimal como fracción (siempre 2 dígitos)
    texto_decimal = f"{decimal:02d}/100"
    
    return f"{texto_entero} con {texto_decimal}"


def convertir_entero(n):
    """Convierte un número entero a texto en español"""
    if n == 0:
        return "Cero"
    
    unidades = ['', 'Uno', 'Dos', 'Tres', 'Cuatro', 'Cinco', 'Seis', 'Siete', 'Ocho', 'Nueve']
    decenas = ['', '', 'Veinte', 'Treinta', 'Cuarenta', 'Cincuenta', 'Sesenta', 'Setenta', 'Ochenta', 'Noventa']
    decenas_especiales = ['Diez', 'Once', 'Doce', 'Trece', 'Catorce', 'Quince', 'Dieciséis', 'Diecisiete', 'Dieciocho', 'Diecinueve']
    centenas = ['', 'Ciento', 'Doscientos', 'Trescientos', 'Cuatrocientos', 'Quinientos', 'Seiscientos', 'Setecientos', 'Ochocientos', 'Novecientos']
    
    if n < 10:
        return unidades[n]
    elif n < 20:
        return decenas_especiales[n - 10]
    elif n < 100:
        d = n // 10
        u = n % 10
        if u == 0:
            return decenas[d]
        elif d == 2:
            # Veintiuno, Veintidós, etc.
            if u == 1:
                return "Veintiuno"
            else:
                return f"Veinti{unidades[u].lower()}"
        else:
            return f"{decenas[d]} y {unidades[u].lower()}"
    elif n < 1000:
        c = n // 100
        resto = n % 100
        if c == 1 and resto == 0:
            return "Cien"
        elif resto == 0:
            return centenas[c]
        else:
            return f"{centenas[c]} {convertir_entero(resto).lower()}"
    elif n < 1000000:
        # Miles
        miles = n // 1000
        resto = n % 1000
        if miles == 1:
            texto_miles = "Mil"
        else:
            texto_miles = f"{convertir_entero(miles)} mil"
        
        if resto == 0:
            return texto_miles
        else:
            return f"{texto_miles} {convertir_entero(resto).lower()}"
    else:
        # Millones (por si acaso)
        millones = n // 1000000
        resto = n % 1000000
        if millones == 1:
            texto_millones = "Un millón"
        else:
            texto_millones = f"{convertir_entero(millones)} millones"
        
        if resto == 0:
            return texto_millones
        else:
            return f"{texto_millones} {convertir_entero(resto).lower()}"

