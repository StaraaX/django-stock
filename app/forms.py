from django.db.models import fields
from django import forms
from .models import FavoriteTab, Categorie, Produit, Client, Fournisseur, BondeCommande, BondeCommandeProduit,Reglement,BlFacture,BlFactureProduit,VenteAuComptoire,Stock,StockProduit,VenteAuComptoireProduit,PaiementCredit





class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = '__all__'


class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = '__all__'
        


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('code_cl','nom_cl','prenom_cl','adr_cl','tel_cl')


class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ('code_fr','nom_fr','prenom_fr','adr_fr','tel_fr')


class BondeCommandeForm(forms.ModelForm):
    class Meta:
        model = BondeCommande
        fields = '__all__'

class BondeCommandeProduitForm(forms.ModelForm):
    class Meta:
        model = BondeCommandeProduit
        fields = ('produit', 'qteProdBC')


class ReglementForm(forms.ModelForm):
    class Meta:
        model = Reglement
        fields =( 'montant_payé',)


class PaiementCreditForm(forms.ModelForm):
    class Meta:
        model = PaiementCredit
        fields =( 'montant_payé',)


class BlFactureForm(forms.ModelForm):
    class Meta:
        model = BlFacture
        fields = ('code_doc','date_doc','fournisseur','remise')  


        

        
class BlFactureProduitForm(forms.ModelForm):
    class Meta:
        model = BlFactureProduit
        fields =('qteprodbl', 'prix_ht', 'prix_vente_fr')
        
     


class VenteAuComptoireForm(forms.ModelForm):    
    class Meta:
        model = VenteAuComptoire
        fields = ('code_vente','date_vente','client')


class VenteAuComptoireProduitForm(forms.ModelForm):
    class Meta:
        model = VenteAuComptoireProduit
        fields = '__all__'  



class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'



