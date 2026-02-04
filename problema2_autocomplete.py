"""
Problema 2: Función de autocompletar

Diseño: Trie (árbol de prefijos) para búsqueda eficiente O(m) por longitud del prefijo.
Diagrama: raíz -> nodos por letra -> nodo con flag 'fin_de_palabra' y hijos.
Métodos: insert(word), autocomplete(prefix).
"""


class TrieNode:
    """Nodo del Trie: hijos por carácter y marca de fin de palabra."""

    __slots__ = ("children", "is_end")

    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.is_end = False


class Autocomplete:
    """
    Autocompletado basado en Trie.
    insert(word): añade una palabra.
    autocomplete(prefix): devuelve todas las palabras que empiezan por prefix.
    """

    def __init__(self) -> None:
        self._root = TrieNode()

    def insert(self, word: str) -> None:
        """Inserta una palabra en el Trie (solo letras; se normaliza a minúsculas)."""
        word = (word or "").strip().lower()
        if not word:
            return
        node = self._root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def _collect_words(self, node: TrieNode, prefix: str, result: list[str]) -> None:
        """Recorre el subárbol y recoge todas las palabras que cuelgan de node."""
        if node.is_end:
            result.append(prefix)
        for char, child in sorted(node.children.items()):
            self._collect_words(child, prefix + char, result)

    def autocomplete(self, prefix: str) -> list[str]:
        """
        Devuelve todas las palabras que empiezan por prefix.
        Si prefix está vacío, devuelve todas las palabras almacenadas.
        """
        prefix = prefix.strip().lower()
        node = self._root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        result: list[str] = []
        self._collect_words(node, prefix, result)
        return sorted(result)

    # Alias en camelCase
    def insert_word(self, word: str) -> None:
        """Alias de insert para compatibilidad con enunciado 'insert(word)'."""
        self.insert(word)
