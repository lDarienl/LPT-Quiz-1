# Resumen para presentar cada problema

Este documento sirve para explicar en una presentación (oral o escrita) cómo funciona cada solución, qué se usó y por qué.

---

## Cómo correr el proyecto (venv + pytest)

```powershell
# Crear entorno virtual
python -m venv .venv

# Activar (PowerShell)
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
python -m pytest test/ -v
```

---

## Problema 1: Sistema de navegación de páginas web

### Qué hace

Simula el comportamiento de un navegador: **atrás**, **adelante** y **cargar página**. El usuario puede ir a una URL, volver a la anterior y avanzar de nuevo.

### Cómo funciona

- Se guarda la **página actual**.
- **Historial “atrás”**: pila con las páginas por las que ya pasamos (para `goBack`).
- **Historial “adelante”**: pila con las páginas a las que podemos volver después de haber hecho “atrás” (para `goForward`).

Flujo:

1. **loadPage(url)**  
   Si hay página actual, se mete en la pila “atrás”. Se vacía la pila “adelante” (como en un navegador real: al navegar a una nueva URL se pierde el “adelante”). La nueva URL pasa a ser la página actual.

2. **goBack()**  
   Si hay páginas en “atrás”, la actual se mueve a “adelante”, se saca la última de “atrás” y esa pasa a ser la actual. Si no hay “atrás”, se devuelve `None`.

3. **goForward()**  
   Si hay páginas en “adelante”, la actual se mueve a “atrás”, se saca la última de “adelante” y esa pasa a ser la actual. Si no hay “adelante”, se devuelve `None`.

### Qué se usó y por qué

- **Dos pilas (listas usadas como stack)**  
  “Atrás” y “adelante” son pilas: solo se usa `append` y `pop`. Así se respeta el orden temporal (última visitada = primera en salir) y el coste de back/forward es O(1).

- **Por qué pilas y no una sola lista con índice**  
  Con una lista y un índice habría que decidir qué pasa al cargar una nueva página (borrar todo lo que está “adelante”). Con dos pilas eso es natural: al cargar una nueva página se vacía la pila “adelante”.

### Casos extremos que se manejan

- **goBack() sin historial**: no hay páginas anteriores → se devuelve `None`.
- **goForward() sin historial**: no hay páginas siguientes → se devuelve `None`.
- **Una sola página cargada**: `goBack()` devuelve `None`.
- **Cargar nueva página**: se limpia “adelante” para no permitir avanzar a URLs que ya no tienen sentido en el flujo actual.

### Dónde está el código

- Clase: `WebBrowser` en **`problema1_navegador.py`**.
- Métodos principales: `loadPage`, `goBack`, `goForward` (y versiones snake_case: `load_page`, `go_back`, `go_forward`).

---

## Problema 2: Función de autocompletar

### Qué hace

Dado un **prefijo** (por ejemplo `"cas"`), devuelve **todas las palabras almacenadas que empiezan por ese prefijo** (ej.: `"casa"`, `"casamiento"`, `"casero"`). Similar al autocompletado de un buscador o un teclado.

### Cómo funciona

- Se usa una estructura **Trie** (árbol de prefijos):
  - Cada nodo tiene hijos por **letra**.
  - Un nodo puede marcar **fin de palabra** (existe una palabra que termina ahí).

- **insert(palabra)**  
  Se recorre el Trie letra a letra, creando nodos si no existen. Al terminar la palabra se marca ese nodo como “fin de palabra”.

- **autocomplete(prefijo)**  
  Se baja por el Trie siguiendo el prefijo. Si en algún momento no hay hijo para una letra, no hay coincidencias → lista vacía. Si se llega al nodo correspondiente al final del prefijo, desde ahí se recorren todos los descendientes y se recogen las palabras que tengan “fin de palabra”.

### Qué se usó y por qué

- **Trie**  
  La búsqueda por prefijo es natural: bajar por el prefijo y luego recorrer un subárbol. No hace falta revisar todas las palabras.
  - Inserción: O(m), con m = longitud de la palabra.
  - Autocompletado: O(m + k), con m = longitud del prefijo y k = número de palabras que coinciden (y su longitud). Mucho mejor que recorrer todas las palabras y filtrar por prefijo.

- **Por qué no solo una lista de palabras**  
  Con una lista, para cada prefijo habría que recorrer todas las palabras y comprobar si empiezan por el prefijo → O(n × longitud media). Con un Trie solo se recorre el camino del prefijo y luego las ramas que tienen palabras.

### Casos que se manejan

- Prefijo que no coincide con ninguna palabra → lista vacía.
- Prefijo vacío → se devuelven todas las palabras almacenadas (recorriendo desde la raíz).
- Palabras vacías o solo espacios en `insert` → se ignoran (no se inserta nada).
- Se normaliza a minúsculas para que la búsqueda sea insensible a mayúsculas.

### Dónde está el código

- Clase del Trie: **`problema2_autocomplete.py`** (`TrieNode` y `Autocomplete`).
- Métodos: `insert(word)` y `autocomplete(prefix)`.

---

## Problema 3: Sistema de recomendación de productos

### Qué hace

Recomienda productos con la idea **“los usuarios que compraron X también compraron Y”**: a partir de las compras del usuario, se buscan otros usuarios con gustos parecidos y se recomiendan productos que ellos compraron y el usuario aún no.

### Cómo funciona

- Se mantienen dos estructuras:
  1. **Usuario → productos**: para cada usuario, el conjunto de productos que ha comprado.
  2. **Producto → usuarios**: para cada producto, el conjunto de usuarios que lo compraron (para encontrar “co-compradores”).

- **addPurchase(usuario, producto)**  
  Se añade el producto al conjunto del usuario y el usuario al conjunto del producto.

- **getRecommendations(usuario)**  
  1. Se obtienen los productos que ya compró el usuario.
  2. Para cada uno de esos productos, se miran los **otros** usuarios que también lo compraron.
  3. De esos usuarios se toman **todos** los productos que compraron.
  4. Se excluyen los que el usuario ya tiene y el propio producto que estamos usando como “puente”.
  5. Se cuentan cuántas veces aparece cada producto recomendado (cuantos más co-compradores lo tengan, más relevante).
  6. Se ordenan por esa puntuación (y desempate por nombre) y se devuelve una lista limitada (por defecto 10).

### Qué se usó y por qué

- **Conjuntos (set)** para usuario–productos y producto–usuarios  
  Evitan duplicados y permiten consultas tipo “¿este usuario compró este producto?” y “¿quién compró este producto?” en tiempo constante.

- **defaultdict(set)**  
  Simplifica el código: no hay que comprobar “si el usuario no existe, crear conjunto vacío”; el diccionario crea el set automáticamente.

- **Conteo por producto (score)**  
  Un producto recomendado por varios co-compradores se considera más relevante; por eso se ordena por frecuencia antes de devolver la lista.

### Casos que se manejan

- Usuario sin compras → lista de recomendaciones vacía.
- Usuario con compras pero sin otros usuarios que hayan comprado lo mismo → lista vacía.
- Varias relaciones usuario–producto → se acumulan en los conjuntos y el conteo de recomendaciones refleja la “fuerza” de cada producto.

### Dónde está el código

- Clase: `ProductRecommender` en **`problema3_recomendador.py`**.
- Métodos: `addPurchase(usuario, producto)` y `getRecommendations(usuario)` (y versiones snake_case).

---

## Guía: dónde y cómo editar / agregar / eliminar

### Problema 1 (navegador)

| Quiero… | Dónde | Cómo |
|--------|--------|------|
| **Agregar** un método (ej. “limpiar historial”) | `problema1_navegador.py`, clase `WebBrowser` | Añadir un método que vacíe `self._back` y `self._forward` y opcionalmente ponga `self._current = None`. |
| **Cambiar** el límite de páginas atrás/adelante | `problema1_navegador.py` | En `load_page`, después de `self._back.append(...)`, hacer `self._back = self._back[-N:]` (mantener solo las últimas N). Igual para `_forward` en `go_back`/`go_forward` si quieres límite también ahí. |
| **Editar** el comportamiento de “atrás” cuando no hay historial | `problema1_navegador.py`, método `go_back` | Ahora devuelve `None`. Si quieres lanzar excepción: `if not self._back: raise ValueError("No hay página anterior")`. |
| **Eliminar** el alias camelCase (solo dejar snake_case) | `problema1_navegador.py` | Borrar los métodos `loadPage`, `goBack`, `goForward` (y en tests usar `load_page`, `go_back`, `go_forward`). |

### Problema 2 (autocompletado)

| Quiero… | Dónde | Cómo |
|--------|--------|------|
| **Agregar** eliminación de palabra | `problema2_autocomplete.py`, clase `Autocomplete` | Añadir método `delete(word)`: bajar por el Trie hasta el nodo final, poner `is_end = False` y opcionalmente podar nodos sin hijos ni `is_end` hacia arriba. |
| **Limitar** número de sugerencias | `problema2_autocomplete.py`, método `autocomplete` | Añadir parámetro `max_results` y en `_collect_words` dejar de añadir a `result` cuando `len(result) >= max_results` (y cortar el recorrido). |
| **Cambiar** a búsqueda sensible a mayúsculas | `problema2_autocomplete.py` | En `insert` y `autocomplete` quitar el `.lower()` (y opcionalmente el `.strip()` si quieres conservar espacios). |
| **Agregar** más palabras desde un archivo | Fuera del módulo (script o test) | Leer el archivo, línea a línea, y llamar `ac.insert(linea)` para cada palabra. El código del Trie no cambia. |

### Problema 3 (recomendador)

| Quiero… | Dónde | Cómo |
|--------|--------|------|
| **Cambiar** el número de recomendaciones | `problema3_recomendador.py`, método `get_recommendations` | El parámetro `max_recommendations` ya existe (por defecto 10). Puedes pasarlo al llamar: `getRecommendations(usuario, 20)`. Para cambiar el valor por defecto, editar la firma: `def get_recommendations(self, user: str, max_recommendations: int = 15)`. |
| **Agregar** “quitar compra” (para devoluciones) | `problema3_recomendador.py`, clase `ProductRecommender` | Nuevo método `remove_purchase(user, product)`: quitar `product` de `self._user_purchases[user]` y `user` de `self._product_buyers[product]`. Comprobar que el usuario/producto existan. |
| **Cambiar** el criterio de orden (ej. solo por nombre) | `problema3_recomendador.py`, método `get_recommendations` | Donde está `key=lambda p: (-score[p], p)`, cambiar a `key=lambda p: p` para ordenar solo por nombre del producto. |
| **Eliminar** recomendaciones de productos que el usuario ya compró | Ya está hecho en la implementación: se excluyen con `other_product not in my_products`. No hace falta cambiar nada. | Si en el futuro añadieras “carrito” sin comprar, podrías pasar un set adicional de “excluir” y filtrar también por ese set. |

### Tests

| Quiero… | Dónde | Cómo |
|--------|--------|------|
| **Agregar** un nuevo caso de prueba | `test/test_p1.py`, `test_p2.py` o `test_p3.py` | Añadir una función `def test_nombre_descriptivo():` y usar `assert` sobre el comportamiento esperado. Ejecutar con `python -m pytest test/ -v`. |
| **Editar** un test que falla tras cambiar el código | El archivo `test/test_pX.py` correspondiente | Ajustar los `assert` al nuevo comportamiento (o corregir el código si el test tiene razón). |
| **Eliminar** un test | El mismo archivo de test | Borrar la función completa de ese test. |

### Documentación y proyecto

| Quiero… | Dónde | Cómo |
|--------|--------|------|
| **Cambiar** dependencias | `requirements.txt` | Añadir líneas con el nombre del paquete (y opcionalmente versión, ej. `pytest>=8.0.0`). No escribir comandos como `pip install`. |
| **Ignorar** más carpetas/archivos en Git | `.gitignore` | Añadir una línea con la ruta o el patrón (ej. `*.tmp`, `datos/`). |
| **Actualizar** los diagramas | `README.md` | Los diagramas están en bloques ```mermaid ... ```. Editar el contenido siguiendo la sintaxis de [Mermaid](https://mermaid.js.org/). |
| **Resumir** para presentar | `PRESENTACION.md` (este archivo) | Editar las secciones “Qué hace”, “Cómo funciona”, “Qué se usó y por qué” y “Dónde está el código” según tus cambios. |

---

## Resumen de una frase por problema

- **Problema 1:** Navegación tipo navegador con dos pilas (atrás y adelante) y la página actual; back/forward en O(1) y manejo de “sin historial”.
- **Problema 2:** Autocompletado con un Trie: inserción y búsqueda por prefijo eficientes sin revisar todas las palabras.
- **Problema 3:** Recomendaciones “quien compró X también compró Y” con conjuntos usuario–producto y producto–usuarios, y orden por frecuencia de co-compra.
