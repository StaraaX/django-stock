from django.db import models
from django.db.models.signals import pre_delete, post_save,post_init,pre_save
from django.dispatch import receiver


class FavoriteTab(models.Model):
  name = models.CharField(max_length=255)
  url = models.URLField()
  order = models.PositiveIntegerField(unique=True)
  is_favorite = models.BooleanField(default=True)
  
  class Meta:
    ordering = ['order']

  def __str__(self):
    return self.name
    #


# --------- main tables----------------------------------------------------------



class Categorie(models.Model):
    code_cat = models.AutoField(primary_key=True)
    designation_cat = models.CharField(max_length=255)
    def __str__(self):
        return self.designation_cat
        
class Produit(models.Model):
   code_produit = models.AutoField(primary_key=True)
   nom_produit = models.CharField(max_length=255)
   type_produit= models.ForeignKey(Categorie, on_delete=models.CASCADE)
   def __str__(self):
        return self.nom_produit




class PaiementCredit(models.Model):
    code_pc = models.AutoField(primary_key=True)
    etat_pc = models.BooleanField(default=True)
    montant_payé = models.FloatField(default=0)
    
    def __str__(self):
        return str(self.code_pc)

    def update_etat_pc(self):
        V=VenteAuComptoire.objects.filter(client__paiement_credit=self)
        total_vente=0
        for item in V:
            total_vente += item.total_vente
        if  self.montant_payé < total_vente:
            self.etat_pc = False
        else:
            self.etat_pc = True
        self.save()

        
class Client(models.Model):
    code_cl = models.AutoField(primary_key=True)
    nom_cl = models.CharField(max_length=254)
    prenom_cl = models.CharField(max_length=255)
    adr_cl = models.CharField(max_length=255)
    tel_cl = models.CharField(max_length=255)
    paiement_credit = models.OneToOneField('PaiementCredit', on_delete=models.CASCADE)

    

    def __str__(self):
        return self.nom_cl + " " + self.prenom_cl

    def save(self, *args, **kwargs):
        if not self.pk:
            self.paiement_credit = PaiementCredit.objects.create()
        super(Client, self).save(*args, **kwargs)


class Reglement(models.Model):
    code_reg = models.AutoField(primary_key=True)
    etat_reg = models.BooleanField(default=False)
    montant_payé = models.FloatField(default=0)


    def __str__(self):
        return str(self.code_reg)

    def update_etat_reg(self):
        blf=BlFacture.objects.filter(fournisseur__reglement=self)
        totalttc_fac=0
        for item in blf:
            totalttc_fac += item.totalttc_fac
        if  self.montant_payé < totalttc_fac:
            self.etat_reg = False
        else:
            self.etat_reg = True
        self.save()





class Fournisseur(models.Model):
    code_fr = models.AutoField(primary_key=True)
    nom_fr = models.CharField(max_length=254)
    prenom_fr = models.CharField(max_length=255)
    adr_fr = models.CharField(max_length=255)
    tel_fr = models.CharField(max_length=255)
    reglement = models.OneToOneField('Reglement', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nom_fr + " " + self.prenom_fr


    def save(self, *args, **kwargs):
        if not self.pk:
            reglement = Reglement.objects.create(code_reg=self.code_fr)
            self.reglement = reglement
        super(Fournisseur, self).save(*args, **kwargs)    

# -------------------------------------------------------------------

class BondeCommande(models.Model):
    code_bc = models.AutoField(primary_key=True)
    fournisseur=models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.code_bc)

# -- liason entre bon de commande et produit-------------------------------------

class BondeCommandeProduit(models.Model):
    primary_key = models.CharField(max_length=255, primary_key=True)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    bon_de_commande = models.ForeignKey(BondeCommande, on_delete=models.CASCADE)
    qteProdBC = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.primary_key = str(self.produit) + str(self.bon_de_commande)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.produit.__str__() + " " + self.bon_de_commande.__str__()


class Stock(models.Model):
    code_etat = models.AutoField(primary_key=True)
    nom_stock = models.CharField(max_length=254)
    benefice = models.FloatField(blank=True,null=True, default=0)
    def __str__(self):
        return self.nom_stock

    def update_benefice(self):
        sp=StockProduit.objects.filter(stock=self)
        total_benefice=0
        blf=BlFacture.objects.filter(stock=self)
        v=VenteAuComptoire.objects.filter(stock=self)
        for item in blf:
            total_benefice -= item.totalttc_fac
        for item in v:
            total_benefice += item.total_vente
        self.benefice = total_benefice



        

    


class StockProduit(models.Model):
    primary_key = models.CharField(max_length=254, primary_key=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    qteDispo = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.primary_key = str(self.stock) + str(self.produit)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.stock.__str__() + " " + self.produit.__str__()




class BlFacture(models.Model):
    code_doc = models.IntegerField(primary_key=True)
    totalht = models.FloatField(default=0)
    totalttc_bl = models.FloatField(default=0)
    totalttc_fac = models.FloatField(default=0)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    date_doc = models.DateTimeField()
    remise = models.FloatField(default=0)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE,default=1)
    def __str__(self):
        return str("Bon N° " + str(self.code_doc))

    def update_totals(self):
        total_ttc_fac = 0
        total_ttc_bl = 0
        total_ht = 0
        remise= self.remise
        
        for produit in self.blfactureproduit_set.all():
            total_ttc_bl += produit.prix_vente_fr * produit.qteprodbl
            total_ht += produit.prix_ht * produit.qteprodbl

        total_ttc_fac = total_ht + (total_ht * 0.19) 
        total_ttc_fac = total_ttc_fac - (remise*total_ttc_fac)/100
        self.totalttc_fac = total_ttc_fac
        total_ttc_bl -= (remise*total_ttc_bl)/100
        self.totalttc_bl = total_ttc_bl
        self.totalht = total_ht
        self.save()    

# -- liason entre bon de livraison et produit-------------------------------------

class BlFactureProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    bl_facture = models.ForeignKey(BlFacture, on_delete=models.CASCADE)
    qteprodbl = models.IntegerField()
    prix_ht = models.FloatField()
    prix_vente_fr = models.FloatField()
    def __str__(self):
        return self.produit.__str__() + " " + self.bl_facture.__str__()




class VenteAuComptoire(models.Model):
    code_vente = models.AutoField(primary_key=True)
    date_vente = models.DateTimeField()
    total_vente = models.FloatField(default=0)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE,default=1)


    def __str__(self):
        return str(self.code_vente) 


    def update_totals(self):
        total_vente = 0
        for produit in self.venteaucomptoireproduit_set.all():
            total_vente += produit.prixU_vente * produit.qte_prod
        self.total_vente = total_vente
        self.save()
    

   





# -- liason entre vente au comptoire et produit-------------------------------------

class VenteAuComptoireProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    vente_au_comptoire = models.ForeignKey(VenteAuComptoire, on_delete=models.CASCADE)
    qte_prod = models.IntegerField()
    prixU_vente = models.FloatField()

    def __str__(self):
     return str(self.produit) + " " + str(self.vente_au_comptoire)

# *****************************************************************************************

@receiver(pre_delete, sender=BlFacture)
def update_reglement_on_delete(sender, instance, **kwargs):
    reglement = instance.fournisseur.reglement
    reglement.montant_payé -= int(instance.totalttc_fac)
    if reglement.montant_payé < 0:
        reglement.montant_payé = 0
    reglement.save()  



@receiver(post_save, sender=Produit)
def update_stock_on_save(sender, instance, created, **kwargs):
    if not created:
        return

    stock = Stock.objects.get(code_etat=1)
    if (stock is None):
        print("YOOOOOOOOOOO")
        stock = Stock.objects.create(nom_stock="Stock Principal",code_etat=1)
    stockproduit = StockProduit.objects.get_or_create(stock=stock, produit=instance)[0]
    stockproduit.save()




@receiver(post_save, sender=BlFactureProduit)
def update_stock_on_save2(sender, instance, **kwargs):
    stock = Stock.objects.get(code_etat=1)
    stockproduit = StockProduit.objects.get_or_create(stock=stock, produit=instance.produit)[0]
    stockproduit.qteDispo += int(instance.qteprodbl)
    stockproduit.save() 
    


@receiver(post_save, sender=VenteAuComptoireProduit)
def update_stock_on_save3(sender, instance, **kwargs):
    stock = Stock.objects.get(code_etat=1)
    stockproduit = StockProduit.objects.get_or_create(stock=stock, produit=instance.produit)[0]
    stockproduit.qteDispo -= int(instance.qte_prod)
    stockproduit.save()





@receiver(pre_delete, sender=VenteAuComptoire)
def update_paiementcredit_on_delete(sender, instance, **kwargs):
    paiementcredit = instance.client.paiement_credit
    if paiementcredit.montant_payé < instance.total_vente:
        paiementcredit.montant_payé = 0
    paiementcredit.montant_payé -= int(instance.total_vente)
    paiementcredit.save()