"""
Problema 3: Sistema de recomendación de productos

Lógica: "Los usuarios que compraron X también compraron Y".
- Por cada usuario guardamos sus compras.
- Para recomendar: miramos qué compró el usuario; por cada producto P,
  miramos qué otros usuarios compraron P y qué más compraron esos usuarios;
  recomendamos esos productos (excluyendo los que el usuario ya tiene).
Diagrama: usuarios -> conjunto de productos; productos -> conjunto de usuarios.
Métodos: addPurchase(usuario, producto), getRecommendations(usuario).
"""

from collections import defaultdict


class ProductRecommender:
    """
    Recomendador tipo "quien compró X también compró Y".
    addPurchase(usuario, producto) registra una compra.
    getRecommendations(usuario) devuelve productos recomendados.
    """

    def __init__(self) -> None:
        # usuario -> set de productos comprados
        self._user_purchases: dict[str, set[str]] = defaultdict(set)
        # producto -> set de usuarios que lo compraron (para co-ocurrencia)
        self._product_buyers: dict[str, set[str]] = defaultdict(set)

    def add_purchase(self, user: str, product: str) -> None:
        """Registra que el usuario compró el producto."""
        user = str(user).strip()
        product = str(product).strip()
        if not user or not product:
            return
        self._user_purchases[user].add(product)
        self._product_buyers[product].add(user)

    def get_recommendations(self, user: str, max_recommendations: int = 10) -> list[str]:
        """
        Recomendaciones para el usuario basadas en "quien compró X también compró Y".
        - Se consideran los productos que ya compró el usuario.
        - Para cada uno, se ven otros usuarios que compraron ese producto.
        - Se recogen los demás productos que compraron esos usuarios.
        - Se ordenan por frecuencia y se excluyen los que el usuario ya tiene.
        """
        user = str(user).strip()
        my_products = self._user_purchases.get(user)
        if not my_products:
            return []

        # product -> cuántas veces aparece como "también comprado"
        score: dict[str, int] = defaultdict(int)

        for product in my_products:
            co_buyers = self._product_buyers.get(product, set())
            for other_user in co_buyers:
                if other_user == user:
                    continue
                for other_product in self._user_purchases.get(other_user, set()):
                    if other_product != product and other_product not in my_products:
                        score[other_product] += 1

        # Ordenar por puntuación descendente y devolver hasta max_recommendations
        sorted_recs = sorted(
            score.keys(),
            key=lambda p: (-score[p], p)
        )
        return sorted_recs[:max_recommendations]

    # Aliases en camelCase como en el enunciado
    def addPurchase(self, user: str, product: str) -> None:
        self.add_purchase(user, product)

    def getRecommendations(self, user: str, max_recommendations: int = 10) -> list[str]:
        return self.get_recommendations(user, max_recommendations)
