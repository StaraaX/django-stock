from django import template

register = template.Library()

@register.filter
def sumtotalttcreglement(value, arg):
    x=0
    for item in value:
        if item.fournisseur.reglement == arg:
            x += item.totalttc_fac
    return x

@register.filter
def sumtotalttcpc(value, arg):
    x=0
    for item in value:
        if item.client.paiement_credit == arg:
            x += item.total_vente
    return x

  

@register.filter
def minus(v1, v2):
    return v1 - v2 

@register.filter
def soldeSupplier(var,a):
   
    x=0
    for item in var:
        if item.fournisseur == a:
            x += item.totalttc_fac
    return x - a.reglement.montant_payé


@register.filter
def soldeClient(var,a):
   
    x=0
    for item in var:
        if item.client == a:
            x += item.total_vente
    return x - a.paiement_credit.montant_payé

    # montant