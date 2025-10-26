
import math

def decimal_a_binario(numero):
    """Convierte un número decimal a binario"""
    if numero == 0:
        return "0"
    
    binario = ""
    temp = int(numero)
    
    while temp > 0:
        residuo = temp % 2
        binario = str(residuo) + binario
        temp = temp // 2
    
    return binario

def decimal_a_octal(numero):
    """Convierte un número decimal a octal"""
    if numero == 0:
        return "0"
    
    octal = ""
    temp = int(numero)
    
    while temp > 0:
        residuo = temp % 8
        octal = str(residuo) + octal
        temp = temp // 8
    
    return octal

def decimal_a_hexadecimal(numero):
    """Convierte un número decimal a hexadecimal"""
    if numero == 0:
        return "0"
    
    hexadecimal = ""
    temp = int(numero)
    digitos_hex = "0123456789ABCDEF"
    
    while temp > 0:
        residuo = temp % 16
        hexadecimal = digitos_hex[residuo] + hexadecimal
        temp = temp // 16
    
    return hexadecimal

def mostrar_proceso_conversion(numero, base, nombre_base):
    """Muestra el proceso de conversión por divisiones sucesivas"""
    print(f"\n{'='*50}")
    print(f"CONVERSIÓN A {nombre_base.upper()} (BASE {base})")
    print(f"{'='*50}")
    print(f"Número decimal: {numero}")
    print(f"\nProceso de divisiones sucesivas:")
    print(f"{'División':<15} {'Cociente':<15} {'Residuo':<15}")
    print("-" * 45)
    
    temp = int(numero)
    divisiones = []
    
    while temp > 0:
        cociente = temp // base
        residuo = temp % base
        
        # Para hexadecimal, convertir residuos mayores a 9
        if base == 16 and residuo > 9:
            residuo_mostrar = chr(65 + residuo - 10)  # A=10, B=11, etc.
        else:
            residuo_mostrar = str(residuo)
        
        divisiones.append((temp, cociente, residuo_mostrar))
        print(f"{temp} ÷ {base:<10} {cociente:<15} {residuo_mostrar:<15}")
        temp = cociente
    
    # Construir resultado leyendo residuos de abajo hacia arriba
    resultado = "".join([str(d[2]) for d in reversed(divisiones)])
    print(f"\nResultado (residuos de abajo hacia arriba): {resultado}")
    print(f"{'='*50}\n")
    
    return resultado

def hoja_principal():
    """Simula la hoja PRINCIPAL de Excel"""
    print("\n" + "="*60)
    print(" "*15 + "CALCULADORA DE CONVERSIONES")
    print("="*60)
    
    while True:
        try:
            numero = float(input("\nIngrese un número decimal (0-1000) o -1 para salir: "))
            
            if numero == -1:
                print("Saliendo...")
                break
            
            if numero < 0 or numero > 1000:
                print("Error: El número debe estar entre 0 y 1000")
                continue
            
            numero_entero = int(numero)
            
            # Realizar conversiones
            binario = decimal_a_binario(numero_entero)
            octal = decimal_a_octal(numero_entero)
            hexadecimal = decimal_a_hexadecimal(numero_entero)
            
            # Mostrar resultados
            print(f"\n{'='*60}")
            print(f"RESULTADOS DE LA CONVERSIÓN")
            print(f"{'='*60}")
            print(f"Decimal:        {numero_entero}")
            print(f"Binario:        {binario}")
            print(f"Octal:          {octal}")
            print(f"Hexadecimal:    {hexadecimal}")
            print(f"{'='*60}")
            
            # Preguntar si desea ver el proceso
            ver_proceso = input("\n¿Desea ver el proceso de conversión? (s/n): ").lower()
            if ver_proceso == 's':
                hoja_trabajo(numero_entero)
            
        except ValueError:
            print("Error: Ingrese un número válido")

def hoja_trabajo(numero):
    """Simula la hoja HTRABAJO de Excel - Muestra el proceso detallado"""
    print("\n" + "="*60)
    print(" "*15 + "HOJA DE TRABAJO - PROCESO DETALLADO")
    print("="*60)
    
    # Mostrar proceso para cada base
    mostrar_proceso_conversion(numero, 2, "binario")
    mostrar_proceso_conversion(numero, 8, "octal")
    mostrar_proceso_conversion(numero, 16, "hexadecimal")

def hoja_prueba():
    """Simula la hoja HOJA PRUEBA de Excel - Casos de prueba"""
    print("\n" + "="*70)
    print(" "*20 + "HOJA DE PRUEBAS")
    print("="*70)
    
    # Casos de prueba predefinidos
    casos_prueba = [
        (0, "0", "0", "0"),
        (1, "1", "1", "1"),
        (10, "1010", "12", "A"),
        (15, "1111", "17", "F"),
        (16, "10000", "20", "10"),
        (100, "1100100", "144", "64"),
        (255, "11111111", "377", "FF"),
        (500, "111110100", "764", "1F4"),
        (1000, "1111101000", "1750", "3E8"),
    ]
    
    print(f"\n{'Decimal':<10} {'Binario':<15} {'Octal':<10} {'Hex':<10} {'Estado':<15}")
    print("-" * 70)
    
    errores = 0
    for decimal, bin_esperado, oct_esperado, hex_esperado in casos_prueba:
        bin_calculado = decimal_a_binario(decimal)
        oct_calculado = decimal_a_octal(decimal)
        hex_calculado = decimal_a_hexadecimal(decimal)
        
        # Verificar si los resultados coinciden
        if (bin_calculado == bin_esperado and 
            oct_calculado == oct_esperado and 
            hex_calculado == hex_esperado):
            estado = "✓ CORRECTO"
        else:
            estado = "✗ ERROR"
            errores += 1
        
        print(f"{decimal:<10} {bin_calculado:<15} {oct_calculado:<10} {hex_calculado:<10} {estado:<15}")
    
    print("-" * 70)
    print(f"\nResultado: {len(casos_prueba) - errores}/{len(casos_prueba)} pruebas exitosas")
    print("="*70 + "\n")

def menu_principal():
    """Menú principal del programa"""
    while True:
        print("\n" + "="*60)
        print(" "*15 + "MENÚ PRINCIPAL")
        print("="*60)
        print("1. Hoja Principal - Calculadora de Conversiones")
        print("2. Hoja de Trabajo - Ver Proceso Detallado")
        print("3. Hoja de Pruebas - Verificar Casos de Prueba")
        print("4. Salir")
        print("="*60)
        
        opcion = input("\nSeleccione una opción (1-4): ")
        
        if opcion == "1":
            hoja_principal()
        elif opcion == "2":
            try:
                numero = int(input("\nIngrese un número decimal para ver su proceso de conversión: "))
                if 0 <= numero <= 1000:
                    hoja_trabajo(numero)
                else:
                    print("Error: El número debe estar entre 0 y 1000")
            except ValueError:
                print("Error: Ingrese un número válido")
        elif opcion == "3":
            hoja_prueba()
        elif opcion == "4":
            print("\n¡Hasta luego!")
            break
        else:
            print("\nOpción inválida. Intente nuevamente.")

# Ejecutar el programa
if __name__ == "__main__":
    print("\n" + "="*60)
    print(" "*10 + "SISTEMA DE CONVERSIÓN DE BASES NUMÉRICAS")
    print("="*60)
    menu_principal()