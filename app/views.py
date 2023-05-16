from django.shortcuts import render,get_object_or_404,redirect
from .models import FavoriteTab, Categorie, Produit, Client, Fournisseur, BondeCommande, BondeCommandeProduit,Reglement,BlFacture,BlFactureProduit,VenteAuComptoire,Stock,StockProduit,VenteAuComptoireProduit,PaiementCredit
from django.contrib.auth import authenticate, login, logout
from .forms import ProduitForm, CategorieForm, ClientForm, FournisseurForm, BondeCommandeForm, BondeCommandeProduitForm, ReglementForm, BlFactureForm, BlFactureProduitForm, VenteAuComptoireForm, VenteAuComptoireProduitForm,StockForm,PaiementCreditForm
from django.contrib import messages
from django import forms
from django.db.models import Sum
from django.contrib.auth.models import User




   

def update_favorite_tab(request, tab_id):
    tab = get_object_or_404(FavoriteTab, pk=tab_id)
    tab.is_favorite = not tab.is_favorite
    tab.save()
    return redirect('myaccount')


def update_username(request):
    username = request.POST['username']
    user = request.user
    user.username = username
    user.save()
    return redirect('myaccount')

def update_password(request):
    user = request.user
    old_password = request.POST['old']
    password = request.POST['password']
    password2 = request.POST['password2']
    if user.check_password(old_password) and password == password2:
        user.set_password(password)
        user.save()
        return redirect('myaccount')
    else:
        return redirect('myaccount')

   

def show_navigation(request):
  # Get the current user's favorite tabs

  if request.user.is_authenticated:
    tabs = FavoriteTab.objects.order_by('order')
    username=request.user.username
    context = {'tabs': tabs, 'username': username}
    return context
  else:
    return redirect('login')
    


def login_view(request):
    if request.user.is_authenticated:
        return redirect('myaccount')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                user.save()
                return redirect('myaccount')
            else:
                error = "Pseudo ou Mot de passe incorrect"
                return render(request, 'login.html', {'error': error})
        except Exception as e:
            error = "Pseudo ou Mot de passe incorrect"
            return render(request, 'login.html', {'error': error})
    else:
        return render(request, 'login.html')


from django.contrib.auth import authenticate, login

def register(request):
    if request.user.is_authenticated:
        return redirect('myaccount')
    if request.method == 'POST':
        username = request.POST['username']
        mail = request.POST['mail']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            try:
                user = User.objects.create_user(username=username, password=password, email=mail, is_staff=True, is_active=True, is_superuser=True)
                user.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('myaccount')
            except Exception as e:
                error2 = "Username already exists"
                return render(request, 'login.html', {'error2': error2})
        else:
            error2 = "Passwords do not match"
            return render(request, 'login.html', {'error2': error2})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



def my_account(request):
    if request.user.is_authenticated:
      tabs=show_navigation(request)
      
      return render(request, 'myaccount.html', {'tabs': tabs})    
    else:
      return redirect('login')


# products 

def products(request):
    if request.user.is_authenticated:
        tabs=show_navigation(request)
        product = Produit.objects.all()
        return render(request, 'products/products.html', {'tabs': tabs, 'products': product})
    else:
      return redirect('login') 


def edit_product(request,pk):
    p=Produit.objects.get(code_produit=pk)
    tabs=show_navigation(request)
    if request.method=='POST':
        form=ProduitForm(request.POST,instance=p)
        if form.is_valid():
            form.save()
            return redirect('products')
    
    else:
        form=ProduitForm(instance=p)
        context={'form':form,'tabs':tabs}
        return render(request,'products/editproduct.html',context)


def delete_product(request,pk):
    p=Produit.objects.get(code_produit=pk)
    tabs=show_navigation(request)
    if request.method=='POST':
        p.delete()
        return redirect('products')    
    context={'item':p,'tabs':tabs}
    return render(request,'products/deleteproduct.html',context)


def add_product(request):
    if request.method =='POST':
        form=ProduitForm(request.POST)
        tabs=show_navigation(request)
        if form.is_valid():
            form.save()
            form=ProduitForm()
            return redirect('products') 
        else:
            return redirect('products')    
    else:
        form=ProduitForm()
        tabs=show_navigation(request)
        return render(request, "products/addproduct.html",{"form":form,"tabs":tabs})

# typeProducts

def typeProducts(request):
    if request.user.is_authenticated:
      tabs=show_navigation(request)
      typeproduct = Categorie.objects.all()
      return render(request, 'typeProducts/typeProducts.html', {'tabs': tabs, 'types': typeproduct})
    
    else:
      return redirect('login') 

def edit_typeProduct(request,tpk):
  
    tp=Categorie.objects.get(code_cat=tpk)
    tabs=show_navigation(request)
    if request.method=='POST':
        form=CategorieForm(request.POST,instance=tp)
        if form.is_valid():
            form.save()
            return redirect('typeproducts')
    
    else:
        form=CategorieForm(instance=tp)
        context={'form':form,'tabs':tabs}
        return render(request,'typeProducts/edittypeProduct.html',context)


def delete_typeProduct(request,tpk):
    tp=Categorie.objects.get(code_cat=tpk)
    tabs=show_navigation(request)
    if request.method=='POST':
        tp.delete()
        return redirect('typeproducts')
    
    context={'item':tp,'tabs':tabs}
    return render(request,'typeProducts/deletetypeProduct.html',context)


def add_typeProduct(request):
    if request.method =='POST':
        form=CategorieForm(request.POST)
        tabs=show_navigation(request)
        if form.is_valid():
            form.save()
            form=CategorieForm()
            return redirect('typeproducts') 
        else:
            
            return redirect('typeproducts')    
    else:
        form=CategorieForm()
        tabs=show_navigation(request)
        return render(request, "typeProducts/addtypeProduct.html",{"form":form,"tabs":tabs})



 # clients


def clients(request):
    if request.user.is_authenticated:
        tabs=show_navigation(request)
        client = Client.objects.all()
        v=VenteAuComptoire.objects.all()
        context={'tabs': tabs, 'clients': client,'v':v}
        return render(request, 'clients/clients.html',context)
    else:
      return redirect('login') 

def edit_client(request,ck):  
    c=Client.objects.get(code_cl=ck)
    tabs=show_navigation(request)
    if request.method=='POST':
        form=ClientForm(request.POST,instance=c)
        if form.is_valid():
            form.save()
            return redirect('clients')
    
    else:
        form=ClientForm(instance=c)
        context={'form':form,'tabs':tabs}
        return render(request,'clients/editclient.html',context)


def delete_client(request,ck):
    c=Client.objects.get(code_cl=ck)
    tabs=show_navigation(request)
    if request.method=='POST':
        c.delete()
        return redirect('clients')
    
    context={'item':c,'tabs':tabs}
    return render(request,'clients/deleteclient.html',context)


def add_client(request):
    if request.method =='POST':
        form=ClientForm(request.POST)
        tabs=show_navigation(request)
        if form.is_valid():
            form.save()
            form=ClientForm()
            return redirect('clients')
        else:
            
            return redirect('clients')
    else:
        form=ClientForm()
        tabs=show_navigation(request)
        return render(request, "clients/addclient.html",{"form":form,"tabs":tabs})

#suppliers

def suppliers(request):
    if request.user.is_authenticated:
        tabs=show_navigation(request)
        supplier = Fournisseur.objects.all()
        reglement = Reglement.objects.all()
        bf = BlFacture.objects.all()
        context = {'tabs': tabs, 'suppliers': supplier, 'bf': bf, 'r': reglement}
        return render(request, 'suppliers/suppliers.html', context)
    else:
      return redirect('login') 



def edit_supplier(request,sk):
    s=Fournisseur.objects.get(code_fr=sk)
    tabs=show_navigation(request)
    if request.method=='POST':
        form=FournisseurForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('suppliers')
    
    else:
        form=FournisseurForm(instance=s)
        context={'form':form,'tabs':tabs}
        return render(request,'suppliers/editsupplier.html',context)


def delete_supplier(request,sk):
    s=Fournisseur.objects.get(code_fr=sk)
    tabs=show_navigation(request)
    if request.method=='POST':
        s.delete()
        return redirect('suppliers')
    
    context={'item':s,'tabs':tabs}
    return render(request,'suppliers/deletesupplier.html',context)


def add_supplier(request):
    if request.method =='POST':
        form=FournisseurForm(request.POST)
        tabs=show_navigation(request)
        if form.is_valid():
            form.save()
            form=FournisseurForm()
            return redirect('suppliers')
        else:
            
            return redirect('suppliers')
    else:
        form=FournisseurForm()
        tabs=show_navigation(request)
        return render(request, "suppliers/addsupplier.html",{"form":form,"tabs":tabs})




# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def bondeCommande(request):
    if request.user.is_authenticated:
        tabs=show_navigation(request)
        bc=BondeCommande.objects.all()
        bp=BondeCommandeProduit.objects.all()
        context={'tabs': tabs, 'bp': bp,'bc':bc}
        return render(request, 'achat/bondecommande/boncommande.html', context)
    else:
      return redirect('login')



def delete_bondeCommande(request,bck):
    b=BondeCommande.objects.get(code_bc=bck)
    tabs=show_navigation(request)
    if request.method=='POST':
        b.delete()
        return redirect('bondecommande') 
    context={'item':b,'tabs':tabs}
    return render(request,'achat/bondeCommande/deletebondeCommande.html',context)


def add_bondeCommande(request):
    if request.method == 'POST':
        form = BondeCommandeForm(request.POST)
        if form.is_valid():
            produits = request.POST.getlist('produits')
            if not produits:
                form.add_error(None, "You must select at least one product.")
                return render(request, 'achat/bondecommande/addbondecommande.html', {'form': form, 'produits': Produit.objects.all()})
            bc = form.save()
            for produit_id in produits:
                quantity = request.POST.get('quantity_' + produit_id)
                bcp = BondeCommandeProduit(produit=Produit.objects.get(pk=produit_id), bon_de_commande=bc, qteProdBC=quantity)
                bcp.save()
            return redirect('bondecommande')
    else:
        form = BondeCommandeForm()
    return render(request, 'achat/bondecommande/addbondecommande.html', {'form': form, 'produits': Produit.objects.all()})


def deleteall_bondeCommande(request):
    b=BondeCommande.objects.all()
    de=True
    tabs=show_navigation(request)
    if request.method=='POST':
        b.delete()
        return redirect('bondecommande')
    context={'item':b,'tabs':tabs,'de':de}
    return render(request,'achat/bondeCommande/deletebondeCommande.html',context)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def bondeLivraison(request):
    if request.user.is_authenticated:
        tabs=show_navigation(request)
        bl=BlFacture.objects.all()
        for b in bl:
            b.update_totals()
        blp=BlFactureProduit.objects.all()
        context={'tabs': tabs, 'blp': blp,'bl':bl}
        return render(request, 'achat/bonLivraison/bonlivraison.html', context)
    else:
      return redirect('login')



def delete_bondeLivraison(request,blk):
    b=BlFacture.objects.get(code_doc=blk)
    tabs=show_navigation(request)
    if request.method=='POST':
        b.delete()
        return redirect('bondelivraison') 
    context={'item':b,'tabs':tabs}
    return render(request,'achat/bonLivraison/deletebondeLivraison.html',context)



def add_bondeLivraison(request):
    if request.method == 'POST':
        form = BlFactureForm(request.POST)
        if form.is_valid():
            produits = request.POST.getlist('produits')
            if not produits:
                form.add_error(None, "You must select at least one product.")
                return render(request, 'achat/bonlivraison/addbonddeLivraison.html', {'form': form, 'produits': Produit.objects.all()})
            bl = form.save()
            total_ttc = 0
            total_ht = 0
            for produit_id in produits:
                quantity = request.POST.get('quantity_' + produit_id)
                priceht= request.POST.get('priceht_' + produit_id)
                pricevt= request.POST.get('pricevt_' + produit_id)
                bcp = BlFactureProduit(produit=Produit.objects.get(pk=produit_id),bl_facture=bl, qteprodbl=quantity, prix_ht=priceht  ,prix_vente_fr=pricevt)
                bcp.save()
                
                
            return redirect('bondelivraison')
    else:
        form = BlFactureForm()
    return render(request, 'achat/bonLivraison/addbondeLivraison.html', {'form': form, 'produits': Produit.objects.all()})



def deleteall_bondeLivraison(request):
    b=BlFacture.objects.all()
    de=True
    tabs=show_navigation(request)
    if request.method=='POST':
        b.delete()
        return redirect('bondelivraison')
    context={'item':b,'tabs':tabs,'de':de}
    return render(request,'achat/bonlivraison/deletebondeLivraison.html',context)


def edit_bondeLivraison(request,blk):
    b=BlFacture.objects.get(code_doc=blk)
    bondelivraison_produits = BlFactureProduit.objects.filter(bl_facture=b)
    tabs=show_navigation(request)
    if request.method=='POST':
        form=BlFactureForm(request.POST,instance=b)
        if form.is_valid():
            form.save()
            for produit in bondelivraison_produits:
                new_quantity = request.POST.get('quantity_' + str(produit.produit))
                new_priceht = request.POST.get('priceht_' + str(produit.produit))
                new_pricevt = request.POST.get('pricevt_' + str(produit.produit))
                print(new_quantity)
                if new_quantity and new_priceht and new_pricevt:
                    produit.qteprodbl = new_quantity
                    produit.prix_ht = new_priceht
                    produit.prix_vente_fr = new_pricevt
                    produit.save()
                    b.update_totals()
            
            return redirect('bondelivraison')
    else:
        form=BlFactureForm(instance=b)
    context={'form':form,'tabs':tabs,'b':b,'produits':bondelivraison_produits}
    return render(request,'achat/bonLivraison/editbondeLivraison.html',context)





# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def facture(request):
    if request.user.is_authenticated:
        tabs=show_navigation(request)
        f=BlFacture.objects.all()
        for i in f:
            i.update_totals()
        fp=BlFactureProduit.objects.all()
        context={'tabs': tabs, 'fp': fp,'f':f}
        return render(request, 'achat/facture/facture.html', context)
    else:
      return redirect('login')



def delete_facture(request,fk):
    f=BlFacture.objects.get(code_doc=fk)
    tabs=show_navigation(request)
    if request.method=='POST':
        f.delete()
        return redirect('facture') 
    context={'item':f,'tabs':tabs}
    return render(request,'achat/facture/deletefacture.html',context)



def add_facture(request):
    if request.method == 'POST':
        form =BlFactureForm(request.POST)
        if form.is_valid():
            produits = request.POST.getlist('produits')
            if not produits:
                form.add_error(None, "You must select at least one product.")
                return render(request, 'achat/facture/addfacture.html', {'form': form, 'produits': Produit.objects.all()})
            f = form.save()
            for produit_id in produits:
                quantity = request.POST.get('quantity_' + produit_id)
                priceht= request.POST.get('priceht_' + produit_id)
                pricevt= request.POST.get('pricevt_' + produit_id)
                bcp = BlFactureProduit(produit=Produit.objects.get(pk=produit_id),bl_facture=f, qteprodbl=quantity, prix_ht=priceht  ,prix_vente_fr=pricevt) 
                bcp.save()
                f.update_totals()
                

            return redirect('facture')
    else:
        form = BlFactureForm()
    return render(request, 'achat/facture/addfacture.html', {'form': form, 'produits': Produit.objects.all()})


def deleteall_facture(request):
    f=BlFacture.objects.all()
    de=True
    tabs=show_navigation(request)
    if request.method=='POST':
        f.delete()
        return redirect('facture')
    context={'item':f,'tabs':tabs,'de':de}
    return render(request,'achat/facture/deletefacture.html',context)


def edit_facture(request,fk):
    f=BlFacture.objects.get(code_doc=fk)
    facture_produits = BlFactureProduit.objects.filter(bl_facture=f)
    tabs=show_navigation(request)
    if request.method=='POST':
        form=BlFactureForm(request.POST,instance=f)
        if form.is_valid():
            form.save()

            for produit in facture_produits:
                new_quantity = request.POST.get('quantity_' + str(produit.produit))
                new_priceht = request.POST.get('priceht_' + str(produit.produit))
                new_pricevt = request.POST.get('pricevt_' + str(produit.produit))
                if new_quantity and new_priceht and new_pricevt:
                    produit.qteprodbl = new_quantity
                    produit.prix_ht = new_priceht
                    produit.prix_vente_fr = new_pricevt
                    produit.save()
                    f.update_totals()
                    
            
            return redirect('facture')
    else:
        form=BlFactureForm(instance=f)
    context={'form':form,'tabs':tabs,'f':f,'produits':facture_produits}
    return render(request,'achat/facture/editfacture.html',context)



# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def reglement(request):
    if request.user.is_authenticated:
        tabs=show_navigation(request)
        r=Reglement.objects.all()
        for i in r:
            i.update_etat_reg()
        bl=BlFacture.objects.all()
        context={'tabs': tabs, 'r':r,'bl':bl}
        return render(request, 'achat/reglement/reglement.html', context)
    else:
      return redirect('login')





def payer_reglement(request,rk):
    r=Reglement.objects.get(code_reg=rk)
    f=Fournisseur.objects.get(reglement=r)
    blf=BlFacture.objects.filter(fournisseur__reglement=r)
    montant=0
    for i in blf :
        montant+=i.totalttc_fac
    tabs=show_navigation(request)
    if request.method=='POST':
        mp=float(request.POST.get('montant_payé'))   
        r.montant_payé += mp
        r.save()
        return redirect('reglement')
    else:
        form=ReglementForm(instance=r)
    context={'form':form,'tabs':tabs,'r':r,'montant':montant,'f':f}
    return render(request,'achat/reglement/payerreglement.html',context)



# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





def stock(request):
    if request.user.is_authenticated:
        tabs=show_navigation(request)
        try:
            s=Stock.objects.get(code_etat='1')
            s.update_benefice()
        except:
            s=Stock.objects.create(code_etat='1',nom_stock='Stock Principal')

        
        sp=StockProduit.objects.all()
        
        
        context={'tabs': tabs, 's':s,'sp':sp}
        return render(request, 'stock/stock.html', context)
    else:
        return redirect('login')


def vente(request):
    if request.user.is_authenticated:
        tabs=show_navigation(request)
        v=VenteAuComptoire.objects.all()
        for i in v:
            i.update_totals()
        vp=VenteAuComptoireProduit.objects.all()
        context={'tabs': tabs, 'vp': vp,'v':v}
        return render(request, 'vente/vente/vente.html', context)
    else:
        return redirect('login') 


def qteDispo(produit):
    sp=StockProduit.objects.filter(produit=produit)
    qteDispo=0
    for i in sp:
        qteDispo+=i.qteDispo
    return qteDispo





def add_vente(request):
    if request.method == 'POST':
        form =VenteAuComptoireForm(request.POST)
        if form.is_valid():
            produits = request.POST.getlist('produits')
            if not produits:
                form.add_error(None, "You must select at least one product.")
                return render(request, 'vente/addvente.html', {'form': form, 'produits': Produit.objects.all()})
            f = form.save()
            for produit_id in produits:
                quantity = request.POST.get('quantity_' + produit_id)
                pricevt= request.POST.get('pricevt_' + produit_id)
                vp =VenteAuComptoireProduit(produit=Produit.objects.get(pk=produit_id),vente_au_comptoire=f, qte_prod=quantity, prixU_vente=pricevt) 
                vp.save()
                f.update_totals()
            return redirect('vente')
    else:
        form = VenteAuComptoireForm()
    produits=Produit.objects.all()
    for i in produits:
        i.qteDispo=qteDispo(produit=i)
    context={'form':form,'produits':produits}
    return render(request, 'vente/vente/addvente.html', context)


def delete_vente(request,vk):
    v=VenteAuComptoire.objects.get(code_vente=vk)
    tabs=show_navigation(request)
    if request.method=='POST':
        v.delete()
        return redirect('vente') 
    context={'item':v,'tabs':tabs}
    return render(request,'vente/vente/deletevente.html',context)


def deleteall_vente(request):
    v=VenteAuComptoire.objects.all()
    tabs=show_navigation(request)
    de=True
    if request.method=='POST':
        v.delete()
        return redirect('vente') 
    context={'item':v,'tabs':tabs,'de':de}
    return render(request,'vente/vente/deletevente.html',context)

def edit_vente(request,vk):
    v=VenteAuComptoire.objects.get(code_vente=vk)
    vente_produits = VenteAuComptoireProduit.objects.filter(vente_au_comptoire=v)
    tabs=show_navigation(request)
    if request.method=='POST':
        form=VenteAuComptoireForm(request.POST,instance=v)
        if form.is_valid():
            form.save()

            for produit in vente_produits:
                new_quantity = request.POST.get('quantity_' + str(produit.produit))
                new_pricevt = request.POST.get('pricevt_' + str(produit.produit))
                if new_quantity and new_pricevt:
                    produit.qte_prod = new_quantity
                    produit.prixU_vente = new_pricevt
                    produit.save()
                    v.update_totals()
                    
            
            return redirect('vente')
    else:
        form=VenteAuComptoireForm(instance=v)
    
    for i in vente_produits:
        i.qteDispo=qteDispo(produit=i.produit)

    
    context={'form':form,'tabs':tabs,'v':v,'vente_produits':vente_produits}
    return render(request,'vente/vente/editvente.html',context)

# --------------------------------------------------------- #



def paiementCredit(request):
    if request.user.is_authenticated:
        tabs=show_navigation(request)
        p=PaiementCredit.objects.all()
        for i in p:
            i.update_etat_pc()
        v=VenteAuComptoire.objects.all()
        context={'tabs': tabs, 'p':p,'v':v}
        return render(request, 'vente/paiement/paiementCredit.html', context)
    else:
      return redirect('login')                


def payer_paiementCredit(request,pck):
    if request.user.is_authenticated:
        p=PaiementCredit.objects.get(code_pc=pck)
        c=Client.objects.get(paiement_credit=p)
        V=VenteAuComptoire.objects.filter(client__paiement_credit=p)
        montant=0
        for i in V :
            montant+=i.total_vente
        tabs=show_navigation(request)
        if request.method=='POST':
            mp=float(request.POST.get('montant_payé'))   
            p.montant_payé += mp
            p.save()
            return redirect('paiementcredit')
        else:
            form=PaiementCreditForm(instance=p)
        context={'form':form,'tabs':tabs,'pc':p,'montant':montant,'c':c}
        return render(request,'vente/paiement/payercredit.html',context)
    else:
      return redirect('login')

   


# --------------------------------------------------------- #

def analyse_achat(request):
    if request.user.is_authenticated:
        tabs=show_navigation(request)
        produits = BlFactureProduit.objects.values("produit__nom_produit").annotate(qte_prod=Sum("qteprodbl"))
        fournisseurs = BlFactureProduit.objects.values("bl_facture__fournisseur__nom_fr","bl_facture__fournisseur__prenom_fr").annotate(qte_prod=Sum("qteprodbl"))
        context={'tabs': tabs,'produits':produits,'fournisseurs':fournisseurs}
        return render(request, 'analyse/achat.html', context)
    else:
      return redirect('login')


def analyse_vente(request):
    if request.user.is_authenticated:
        tabs=show_navigation(request)
        produits = VenteAuComptoireProduit.objects.values("produit__nom_produit").annotate(qte_prod=Sum("qte_prod"))
        clients = VenteAuComptoireProduit.objects.values("vente_au_comptoire__client__nom_cl","vente_au_comptoire__client__prenom_cl").annotate(qte_prod=Sum("qte_prod"))
        context={'tabs': tabs,'produits':produits,'clients':clients}
        
        return render(request, 'analyse/vente.html', context)
    else:
      return redirect('login')