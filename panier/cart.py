from decimal import Decimal
from produits.models import Produit


class Panier:
    def __init__(self, request):
        self.session = request.session
        panier = self.session.get('panier')
        if panier is None:
            panier = self.session['panier'] = {}
        self.panier = panier

    def ajouter(self, produit, quantite=1):
        produit_id = str(produit.id)
        if produit_id not in self.panier:
            self.panier[produit_id] = {
                'quantite': 0,
                'prix': str(produit.prix),
            }
        self.panier[produit_id]['quantite'] += quantite
        self._sauvegarder()

    def modifier(self, produit, quantite):
        produit_id = str(produit.id)
        if produit_id in self.panier:
            self.panier[produit_id]['quantite'] = quantite
            self._sauvegarder()

    def supprimer(self, produit):
        produit_id = str(produit.id)
        if produit_id in self.panier:
            del self.panier[produit_id]
            self._sauvegarder()

    def vider(self):
        del self.session['panier']
        self.session.modified = True

    def _sauvegarder(self):
        self.session.modified = True

    def __iter__(self):
        produit_ids = self.panier.keys()
        produits = Produit.objects.filter(id__in=produit_ids)
        produits_map = {str(p.id): p for p in produits}

        for produit_id, data in self.panier.items():
            if produit_id not in produits_map:
                continue
            item = data.copy()
            item['produit'] = produits_map[produit_id]
            item['prix'] = Decimal(data['prix'])
            item['total_ligne'] = item['prix'] * item['quantite']
            item['produit_id'] = int(produit_id)
            yield item

    def __len__(self):
        return sum(item['quantite'] for item in self.panier.values())

    def total(self):
        return sum(Decimal(item['prix']) * item['quantite'] for item in self.panier.values())
