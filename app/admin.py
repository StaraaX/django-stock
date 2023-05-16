from django.contrib import admin
from .models import FavoriteTab, Categorie, Produit, Client, Fournisseur, BondeCommande, BondeCommandeProduit,Reglement,BlFacture,BlFactureProduit,VenteAuComptoire,Stock,StockProduit,VenteAuComptoireProduit,PaiementCredit

admin.site.register(FavoriteTab)
admin.site.register(Categorie)
admin.site.register(Produit)
admin.site.register(Client)
admin.site.register(Fournisseur)
admin.site.register(BondeCommande)
admin.site.register(BondeCommandeProduit)
admin.site.register(Reglement)
admin.site.register(BlFacture)
admin.site.register(BlFactureProduit)
admin.site.register(VenteAuComptoire)
admin.site.register(Stock)
admin.site.register(StockProduit)
admin.site.register(VenteAuComptoireProduit)
admin.site.register(PaiementCredit)



# Register your models here.
