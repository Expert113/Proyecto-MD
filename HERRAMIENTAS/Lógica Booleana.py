

# Proyecto MD - Calculadora booleana con simplificación y mapa de Karnaugh

# Integrantes:
# Carlos Colorado García
# Jesús Antonio Cobos Juarez
# Jesus Joel Hernández Rivera

# Bibliotecas y módulos necesarios:

import re
from itertools import product
from typing import List, Dict, Tuple

class CalculadoraBooleana:
    def __init__(self, expresion: str):
        self.expresion_original = expresion
        self.variables = self._identificar_variables(expresion)
        self.n_vars = len(self.variables)
        
    def _identificar_variables(self, expr: str) -> List[str]:
        """Identifica todas las variables en la expresión"""
        # Buscar letras que no sean operadores
        variables = set()
        i = 0
        while i < len(expr):
            if expr[i].isalpha() and expr[i] not in ['y', 'v']:
                variables.add(expr[i])
            i += 1
        return sorted(list(variables))
    
    def _reemplazar_variables(self, expr: str, valores: Dict[str, bool]) -> str:
        """Reemplaza variables por sus valores"""
        resultado = ""
        i = 0
        while i < len(expr):
            char = expr[i]
            if char in self.variables:
                resultado += "True" if valores[char] else "False"
            else:
                resultado += char
            i += 1
        return resultado
    
    def _evaluar(self, valores: Dict[str, bool]) -> bool:
        """Evalúa la expresión con los valores dados"""
        expr = self.expresion_original.replace(' ', '')
        
        # Paso 1: Reemplazar variables por valores
        expr = self._reemplazar_variables(expr, valores)
        
        # Paso 2: Procesar NOT (~)
        while '~True' in expr or '~False' in expr:
            expr = expr.replace('~True', 'False')
            expr = expr.replace('~False', 'True')
        
        # Paso 3: Convertir operadores a Python
        # Reemplazar operadores en orden correcto
        expr = expr.replace('y', ' and ')
        expr = expr.replace('v', ' or ')
        
        # Paso 4: Manejar condicionales
        # A --> B = (not A) or B
        while '-->' in expr:
            # Buscar patrones simples primero
            pattern = r'(True|False)\s*-->\s*(True|False)'
            match = re.search(pattern, expr)
            if match:
                a_str, b_str = match.groups()
                a = (a_str == 'True')
                b = (b_str == 'True')
                resultado = (not a) or b
                expr = expr[:match.start()] + str(resultado) + expr[match.end():]
            else:
                # Si no hay patrón simple, buscar con paréntesis
                pattern = r'\((True|False)\)\s*-->\s*\((True|False)\)'
                match = re.search(pattern, expr)
                if match:
                    a_str, b_str = match.groups()
                    a = (a_str == 'True')
                    b = (b_str == 'True')
                    resultado = (not a) or b
                    expr = expr[:match.start()] + str(resultado) + expr[match.end():]
                else:
                    break
        
        # Paso 5: Manejar bicondicionales
        # A <--> B = (A and B) or (not A and not B)
        while '<-->' in expr:
            pattern = r'(True|False)\s*<-->\s*(True|False)'
            match = re.search(pattern, expr)
            if match:
                a_str, b_str = match.groups()
                a = (a_str == 'True')
                b = (b_str == 'True')
                resultado = (a == b)
                expr = expr[:match.start()] + str(resultado) + expr[match.end():]
            else:
                pattern = r'\((True|False)\)\s*<-->\s*\((True|False)\)'
                match = re.search(pattern, expr)
                if match:
                    a_str, b_str = match.groups()
                    a = (a_str == 'True')
                    b = (b_str == 'True')
                    resultado = (a == b)
                    expr = expr[:match.start()] + str(resultado) + expr[match.end():]
                else:
                    break
        
        # Paso 6: Evaluar expresión Python
        try:
            resultado = eval(expr)
            return bool(resultado)
        except Exception as e:
            print(f"Error evaluando: {expr}")
            print(f"Error: {e}")
            return False
    
    def generar_tabla_verdad(self) -> Tuple[List[List], List[bool]]:
        """Genera la tabla de verdad completa"""
        combinaciones = list(product([False, True], repeat=self.n_vars))
        resultados = []
        
        tabla = []
        for comb in combinaciones:
            valores = dict(zip(self.variables, comb))
            resultado = self._evaluar(valores)
            fila = list(comb) + [resultado]
            tabla.append(fila)
            resultados.append(resultado)
        
        return tabla, resultados
    
    def generar_mapa_karnaugh(self, resultados: List[bool]) -> str:
        """Genera el mapa de Karnaugh según el número de variables"""
        if self.n_vars <= 1:
            return self._karnaugh_1var(resultados)
        elif self.n_vars == 2:
            return self._karnaugh_2var(resultados)
        elif self.n_vars == 3:
            return self._karnaugh_3var(resultados)
        elif self.n_vars == 4:
            return self._karnaugh_4var(resultados)
        elif self.n_vars == 5:
            return self._karnaugh_5var(resultados)
        else:
            return "Mapa de Karnaugh no disponible para más de 5 variables"
    
    def _karnaugh_1var(self, res: List[bool]) -> str:
        v = self.variables[0]
        return f"""
Mapa de Karnaugh (1 variable):
     {v}
  0 | {int(res[0])}
  1 | {int(res[1])}
"""
    
    def _karnaugh_2var(self, res: List[bool]) -> str:
        v1, v2 = self.variables
        return f"""
Mapa de Karnaugh (2 variables):
        {v2}
      0  1
  {v1} ┌─────┐
  0 │ {int(res[0])} {int(res[1])} │
  1 │ {int(res[2])} {int(res[3])} │
    └─────┘
"""
    
    def _karnaugh_3var(self, res: List[bool]) -> str:
        v1, v2, v3 = self.variables
        # Orden Gray para columnas: 00, 01, 11, 10
        indices = [0, 1, 3, 2, 4, 5, 7, 6]
        valores = [res[i] for i in indices]
        return f"""
Mapa de Karnaugh (3 variables):
           {v2}{v3}
        00 01 11 10
  {v1} ┌──────────┐
  0 │ {int(valores[0])}  {int(valores[1])}  {int(valores[2])}  {int(valores[3])} │
  1 │ {int(valores[4])}  {int(valores[5])}  {int(valores[6])}  {int(valores[7])} │
    └──────────┘
"""
    
    def _karnaugh_4var(self, res: List[bool]) -> str:
        v1, v2, v3, v4 = self.variables
        # Orden Gray para filas y columnas
        indices = [
            0, 1, 3, 2,
            4, 5, 7, 6,
            12, 13, 15, 14,
            8, 9, 11, 10
        ]
        valores = [res[i] for i in indices]
        return f"""
Mapa de Karnaugh (4 variables):
            {v3}{v4}
         00 01 11 10
  {v1}{v2} ┌──────────┐
  00 │ {int(valores[0])}  {int(valores[1])}  {int(valores[2])}  {int(valores[3])} │
  01 │ {int(valores[4])}  {int(valores[5])}  {int(valores[6])}  {int(valores[7])} │
  11 │ {int(valores[8])}  {int(valores[9])}  {int(valores[10])}  {int(valores[11])} │
  10 │ {int(valores[12])}  {int(valores[13])}  {int(valores[14])}  {int(valores[15])} │
     └──────────┘
"""
    
    def _karnaugh_5var(self, res: List[bool]) -> str:
        v1, v2, v3, v4, v5 = self.variables
        # Dos mapas de 4x4 para 5 variables
        indices_0 = [0, 1, 3, 2, 4, 5, 7, 6, 12, 13, 15, 14, 8, 9, 11, 10]
        indices_1 = [16, 17, 19, 18, 20, 21, 23, 22, 28, 29, 31, 30, 24, 25, 27, 26]
        
        valores_0 = [res[i] for i in indices_0]
        valores_1 = [res[i] for i in indices_1]
        
        return f"""
Mapa de Karnaugh (5 variables):

{v1}=0           {v3}{v4}
         00 01 11 10
  {v2}{v5} ┌──────────┐
  00 │ {int(valores_0[0])}  {int(valores_0[1])}  {int(valores_0[2])}  {int(valores_0[3])} │
  01 │ {int(valores_0[4])}  {int(valores_0[5])}  {int(valores_0[6])}  {int(valores_0[7])} │
  11 │ {int(valores_0[8])}  {int(valores_0[9])}  {int(valores_0[10])}  {int(valores_0[11])} │
  10 │ {int(valores_0[12])}  {int(valores_0[13])}  {int(valores_0[14])}  {int(valores_0[15])} │
     └──────────┘

{v1}=1           {v3}{v4}
         00 01 11 10
  {v2}{v5} ┌──────────┐
  00 │ {int(valores_1[0])}  {int(valores_1[1])}  {int(valores_1[2])}  {int(valores_1[3])} │
  01 │ {int(valores_1[4])}  {int(valores_1[5])}  {int(valores_1[6])}  {int(valores_1[7])} │
  11 │ {int(valores_1[8])}  {int(valores_1[9])}  {int(valores_1[10])}  {int(valores_1[11])} │
  10 │ {int(valores_1[12])}  {int(valores_1[13])}  {int(valores_1[14])}  {int(valores_1[15])} │
     └──────────┘
"""
    
    def simplificar_quine_mccluskey(self, resultados: List[bool]) -> str:
        """Simplifica usando método Quine-McCluskey (versión básica)"""
        # Obtener mintérminos (donde el resultado es True)
        minterms = [i for i, r in enumerate(resultados) if r]
        
        if not minterms:
            return "0"
        if len(minterms) == 2**self.n_vars:
            return "1"
        
        # Simplificación básica
        terminos = []
        for m in minterms:
            binario = format(m, f'0{self.n_vars}b')
            termino = []
            for i, bit in enumerate(binario):
                if bit == '1':
                    termino.append(self.variables[i])
                else:
                    termino.append(f'~{self.variables[i]}')
            terminos.append('(' + ' y '.join(termino) + ')')
        
        if len(terminos) <= 6:
            return ' v '.join(terminos)
        else:
            return f"{terminos[0]} v ... v {terminos[-1]} [{len(terminos)} términos]"
    
    def mostrar_resultados(self):
        """Muestra todos los resultados del análisis"""
        print("="*70)
        print("CALCULADORA DE ÁLGEBRA BOOLEANA")
        print("="*70)
        print(f"\nExpresión original: {self.expresion_original}")
        print(f"\n1. VARIABLES IDENTIFICADAS: {', '.join(self.variables)}")
        print(f"   Total: {self.n_vars} variable(s)")
        
        print("\n2. TABLA DE VERDAD:")
        print("-" * 70)
        tabla, resultados = self.generar_tabla_verdad()
        
        # Encabezado
        header = " | ".join(self.variables) + " | Resultado"
        print(header)
        print("-" * len(header))
        
        # Filas
        for fila in tabla:
            valores_str = " | ".join(["1" if v else "0" for v in fila[:-1]])
            resultado_str = "1" if fila[-1] else "0"
            print(f"{valores_str} |     {resultado_str}")
        
        print("\n3. MAPA DE KARNAUGH:")
        print("-" * 70)
        print(self.generar_mapa_karnaugh(resultados))
        
        print("\n4. EXPRESIÓN SIMPLIFICADA (Forma normal disyuntiva):")
        print("-" * 70)
        expr_simplificada = self.simplificar_quine_mccluskey(resultados)
        print(f"   {expr_simplificada}")
        print("\n" + "="*70)


# Ejemplo de uso
if __name__ == "__main__":
    print("\nIngresa una expresión booleana.")
    print("Operadores: y (AND), v (OR), ~ (NOT), --> (condicional), <--> (bicondicional)")
    print("\nEjemplo: (P y Q) v (~S <--> T)")
    
    expresion = input("\nExpresión: ")
    
    try:
        calc = CalculadoraBooleana(expresion)
        calc.mostrar_resultados()
    except Exception as e:
        print(f"\nError al procesar la expresión: {e}")
        import traceback
        traceback.print_exc()
        print("Verifica que la expresión esté correctamente escrita.")
