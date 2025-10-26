
import re
from typing import Dict, List, Tuple, Optional

class SolucionadorConjuntos:
    """
    Resuelve problemas de teoría de conjuntos con 2 o 3 categorías
    Ejemplo: preferencias de helados, deportes, materias, etc.
    """
    
    def __init__(self):
        self.total = 0
        self.categoria_a = ""
        self.categoria_b = ""
        self.categoria_c = ""
        self.solo_a = 0
        self.solo_b = 0
        self.solo_c = 0
        self.a_y_b = 0
        self.a_y_c = 0
        self.b_y_c = 0
        self.todos = 0
        self.ninguno = 0
        self.tiene_tres_categorias = False
    
    def problema_dos_conjuntos(self, total: int, solo_a: int, solo_b: int, 
                               ninguno: int, cat_a: str = "A", cat_b: str = "B"):
        """
        Resuelve problema con 2 conjuntos (como el ejemplo del helado)
        
        Parámetros:
        - total: total de elementos
        - solo_a: elementos que solo pertenecen al conjunto A
        - solo_b: elementos que solo pertenecen al conjunto B
        - ninguno: elementos que no pertenecen a ningún conjunto
        - cat_a, cat_b: nombres de las categorías
        """
        self.total = total
        self.solo_a = solo_a
        self.solo_b = solo_b
        self.ninguno = ninguno
        self.categoria_a = cat_a
        self.categoria_b = cat_b
        self.tiene_tres_categorias = False
        
        # Calcular elementos que pertenecen a ambos conjuntos
        con_preferencia = total - ninguno
        solo_uno = solo_a + solo_b
        self.a_y_b = con_preferencia - solo_uno
        
        # Validar
        if self.a_y_b < 0:
            raise ValueError("Los datos son inconsistentes. Revisa los números.")
        
        return self._generar_reporte_dos()
    
    def problema_dos_conjuntos_con_ambos(self, total: int, solo_a: int, solo_b: int,
                                         ambos: int, cat_a: str = "A", cat_b: str = "B"):
        """
        Resuelve cuando te dan directamente cuántos están en ambos conjuntos
        """
        self.total = total
        self.solo_a = solo_a
        self.solo_b = solo_b
        self.a_y_b = ambos
        self.categoria_a = cat_a
        self.categoria_b = cat_b
        self.tiene_tres_categorias = False
        
        # Calcular los que no están en ninguno
        self.ninguno = total - (solo_a + solo_b + ambos)
        
        if self.ninguno < 0:
            raise ValueError("Los datos son inconsistentes. La suma supera el total.")
        
        return self._generar_reporte_dos()
    
    def problema_tres_conjuntos(self, total: int, solo_a: int = 0, solo_b: int = 0,
                                solo_c: int = 0, a_y_b: int = 0, a_y_c: int = 0,
                                b_y_c: int = 0, todos: int = 0, ninguno: int = 0,
                                cat_a: str = "A", cat_b: str = "B", cat_c: str = "C"):
        """
        Resuelve problemas con 3 conjuntos (más complejo)
        Usa el principio de inclusión-exclusión
        """
        self.total = total
        self.solo_a = solo_a
        self.solo_b = solo_b
        self.solo_c = solo_c
        self.a_y_b = a_y_b
        self.a_y_c = a_y_c
        self.b_y_c = b_y_c
        self.todos = todos
        self.ninguno = ninguno
        self.categoria_a = cat_a
        self.categoria_b = cat_b
        self.categoria_c = cat_c
        self.tiene_tres_categorias = True
        
        return self._generar_reporte_tres()
    
    def _generar_reporte_dos(self) -> Dict:
        """Genera reporte para 2 conjuntos"""
        total_a = self.solo_a + self.a_y_b
        total_b = self.solo_b + self.a_y_b
        
        return {
            'total': self.total,
            'solo_' + self.categoria_a: self.solo_a,
            'solo_' + self.categoria_b: self.solo_b,
            'ambos': self.a_y_b,
            'ninguno': self.ninguno,
            'total_' + self.categoria_a: total_a,
            'total_' + self.categoria_b: total_b,
            'porcentaje_' + self.categoria_a: round(total_a / self.total * 100, 2),
            'porcentaje_' + self.categoria_b: round(total_b / self.total * 100, 2),
            'solucion_texto': self._texto_solucion_dos()
        }
    
    def _texto_solucion_dos(self) -> str:
        """Genera explicación paso a paso"""
        total_a = self.solo_a + self.a_y_b
        total_b = self.solo_b + self.a_y_b
        
        texto = f"""
SOLUCIÓN PASO A PASO:
==========================================

DATOS:
- Total: {self.total}
- Solo {self.categoria_a}: {self.solo_a}
- Solo {self.categoria_b}: {self.solo_b}
- Ninguno: {self.ninguno}

CÁLCULOS:
1. Personas con al menos una preferencia:
   {self.total} - {self.ninguno} = {self.total - self.ninguno}

2. Personas con solo una preferencia:
   {self.solo_a} + {self.solo_b} = {self.solo_a + self.solo_b}

3. Personas con AMBAS preferencias:
   {self.total - self.ninguno} - {self.solo_a + self.solo_b} = {self.a_y_b}

RESULTADOS:
✓ Solo {self.categoria_a}: {self.solo_a}
✓ Solo {self.categoria_b}: {self.solo_b}
✓ Ambos ({self.categoria_a} y {self.categoria_b}): {self.a_y_b}
✓ Ninguno: {self.ninguno}

TOTALES:
→ Total que les gusta {self.categoria_a}: {self.solo_a} + {self.a_y_b} = {total_a} ({round(total_a/self.total*100, 1)}%)
→ Total que les gusta {self.categoria_b}: {self.solo_b} + {self.a_y_b} = {total_b} ({round(total_b/self.total*100, 1)}%)

VERIFICACIÓN:
{self.solo_a} + {self.solo_b} + {self.a_y_b} + {self.ninguno} = {self.solo_a + self.solo_b + self.a_y_b + self.ninguno} ✓
"""
        return texto
    
    def _generar_reporte_tres(self) -> Dict:
        """Genera reporte para 3 conjuntos"""
        total_a = self.solo_a + self.a_y_b + self.a_y_c + self.todos
        total_b = self.solo_b + self.a_y_b + self.b_y_c + self.todos
        total_c = self.solo_c + self.a_y_c + self.b_y_c + self.todos
        
        return {
            'total': self.total,
            'solo_' + self.categoria_a: self.solo_a,
            'solo_' + self.categoria_b: self.solo_b,
            'solo_' + self.categoria_c: self.solo_c,
            self.categoria_a + '_y_' + self.categoria_b: self.a_y_b,
            self.categoria_a + '_y_' + self.categoria_c: self.a_y_c,
            self.categoria_b + '_y_' + self.categoria_c: self.b_y_c,
            'los_tres': self.todos,
            'ninguno': self.ninguno,
            'total_' + self.categoria_a: total_a,
            'total_' + self.categoria_b: total_b,
            'total_' + self.categoria_c: total_c,
            'solucion_texto': self._texto_solucion_tres()
        }
    
    def _texto_solucion_tres(self) -> str:
        """Genera explicación para 3 conjuntos"""
        total_a = self.solo_a + self.a_y_b + self.a_y_c + self.todos
        total_b = self.solo_b + self.a_y_b + self.b_y_c + self.todos
        total_c = self.solo_c + self.a_y_c + self.b_y_c + self.todos
        
        texto = f"""
SOLUCIÓN PASO A PASO (3 CONJUNTOS):
==========================================

DATOS:
- Total: {self.total}
- Solo {self.categoria_a}: {self.solo_a}
- Solo {self.categoria_b}: {self.solo_b}
- Solo {self.categoria_c}: {self.solo_c}
- {self.categoria_a} y {self.categoria_b} (sin {self.categoria_c}): {self.a_y_b}
- {self.categoria_a} y {self.categoria_c} (sin {self.categoria_b}): {self.a_y_c}
- {self.categoria_b} y {self.categoria_c} (sin {self.categoria_a}): {self.b_y_c}
- Los tres: {self.todos}
- Ninguno: {self.ninguno}

TOTALES:
→ Total {self.categoria_a}: {self.solo_a} + {self.a_y_b} + {self.a_y_c} + {self.todos} = {total_a}
→ Total {self.categoria_b}: {self.solo_b} + {self.a_y_b} + {self.b_y_c} + {self.todos} = {total_b}
→ Total {self.categoria_c}: {self.solo_c} + {self.a_y_c} + {self.b_y_c} + {self.todos} = {total_c}

VERIFICACIÓN:
{self.solo_a} + {self.solo_b} + {self.solo_c} + {self.a_y_b} + {self.a_y_c} + {self.b_y_c} + {self.todos} + {self.ninguno} = {self.solo_a + self.solo_b + self.solo_c + self.a_y_b + self.a_y_c + self.b_y_c + self.todos + self.ninguno} ✓
"""
        return texto
    
    def diagrama_venn_ascii(self) -> str:
        """Genera un diagrama de Venn simple en ASCII"""
        if not self.tiene_tres_categorias:
            return f"""
    Diagrama de Venn (2 conjuntos):
    
           ┌─────────────────┐
           │   Solo {self.categoria_a}    │
           │      {self.solo_a}        │
    ┌──────┼─────────┬───────┼──────┐
    │      │ Ambos   │       │      │
    │      │   {self.a_y_b}    │       │      │
    └──────┼─────────┴───────┼──────┘
           │   Solo {self.categoria_b}    │
           │      {self.solo_b}        │
           └─────────────────┘
    
    Fuera de los círculos: {self.ninguno} (ninguno)
"""
        else:
            return f"""
    Diagrama de Venn (3 conjuntos):
    
            {self.categoria_a}: {self.solo_a} solo
            {self.categoria_b}: {self.solo_b} solo
            {self.categoria_c}: {self.solo_c} solo
            {self.categoria_a}∩{self.categoria_b}: {self.a_y_b}
            {self.categoria_a}∩{self.categoria_c}: {self.a_y_c}
            {self.categoria_b}∩{self.categoria_c}: {self.b_y_c}
            {self.categoria_a}∩{self.categoria_b}∩{self.categoria_c}: {self.todos}
            Ninguno: {self.ninguno}
"""


# ============================================
# EJEMPLOS DE USO
# ============================================

if __name__ == "__main__":
    solver = SolucionadorConjuntos()
    
    print("="*60)
    print("EJEMPLO 1: Problema del helado")
    print("="*60)
    
    resultado = solver.problema_dos_conjuntos(
        total=50,
        solo_a=10,
        solo_b=5,
        ninguno=20,
        cat_a="Fresa",
        cat_b="Chocolate"
    )
    
    print(resultado['solucion_texto'])
    print(solver.diagrama_venn_ascii())
    
    print("\n" + "="*60)
    print("EJEMPLO 2: Deportes favoritos")
    print("="*60)
    
    # En un grupo de 80 estudiantes:
    # 25 solo juegan fútbol
    # 15 solo juegan basketball
    # 12 juegan ambos deportes
    
    resultado2 = solver.problema_dos_conjuntos_con_ambos(
        total=80,
        solo_a=25,
        solo_b=15,
        ambos=12,
        cat_a="Fútbol",
        cat_b="Basketball"
    )
    
    print(resultado2['solucion_texto'])
    
    print("\n" + "="*60)
    print("EJEMPLO 3: Tres materias favoritas")
    print("="*60)
    
    # En un salón de 100 alumnos:
    resultado3 = solver.problema_tres_conjuntos(
        total=100,
        solo_a=15,      # Solo Matemáticas
        solo_b=20,      # Solo Ciencias
        solo_c=10,      # Solo Historia
        a_y_b=8,        # Matemáticas y Ciencias (sin Historia)
        a_y_c=5,        # Matemáticas e Historia (sin Ciencias)
        b_y_c=7,        # Ciencias e Historia (sin Matemáticas)
        todos=3,        # Las tres materias
        ninguno=32,     # Ninguna de las tres
        cat_a="Matemáticas",
        cat_b="Ciencias",
        cat_c="Historia"
    )
    
    print(resultado3['solucion_texto'])
    print(solver.diagrama_venn_ascii())
    
    print("\n" + "="*60)
    print("EJEMPLO 4: Mascotas")
    print("="*60)
    
    # En un edificio de 60 departamentos:
    # 18 solo tienen perros
    # 12 solo tienen gatos
    # 25 no tienen mascotas
    
    resultado4 = solver.problema_dos_conjuntos(
        total=60,
        solo_a=18,
        solo_b=12,
        ninguno=25,
        cat_a="Perros",
        cat_b="Gatos"
    )
    
    print(resultado4['solucion_texto'])
    print(solver.diagrama_venn_ascii())