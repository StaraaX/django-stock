from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('myaccount/', views.my_account, name='myaccount'),
    path('myaccount/update_username/', views.update_username, name='update_username'),
    path('myaccount/update_password/', views.update_password, name='update_password'),
    path('update_favorite_tab/<int:tab_id>/', views.update_favorite_tab, name='update_favorite_tab'),
    # products
    path('products/', views.products, name='products'),
    path('products/edit/<int:pk>/', views.edit_product, name='editP'),
    path('products/delete/<int:pk>/', views.delete_product, name='deleteP'),
    path('products/add/', views.add_product, name='addP'),
    # typeProducts
    path('typeproducts/', views.typeProducts, name='typeproducts'),
    path('typeproducts/edit/<int:tpk>/', views.edit_typeProduct, name='editTP'),
    path('typeproducts/delete/<int:tpk>/', views.delete_typeProduct, name='deleteTP'),
    path('typeproducts/add/', views.add_typeProduct, name='addTP'),
    # clients
    path('clients/', views.clients, name='clients'),
    path('clients/edit/<int:ck>/', views.edit_client, name='editC'),
    path('clients/delete/<int:ck>/', views.delete_client, name='deleteC'),
    path('clients/add/', views.add_client, name='addC'),
    # suppliers
    path('suppliers/', views.suppliers, name='suppliers'),
    path('suppliers/edit/<int:sk>/', views.edit_supplier, name='editS'),
    path('suppliers/delete/<int:sk>/', views.delete_supplier, name='deleteS'),
    path('suppliers/add/', views.add_supplier, name='addS'),
    
    # bon de commande
    path('bondecommande/', views.bondeCommande, name='bondecommande'),
    path('bondecommande/delete/<int:bck>/', views.delete_bondeCommande, name='deleteBC'),
    path('bondecommande/deleteall/', views.deleteall_bondeCommande, name='deleteAllBC'),
    path('bondecommande/add/', views.add_bondeCommande, name='addBC'),

    # bon de livraison
    path('bondelivraison/', views.bondeLivraison, name='bondelivraison'),
    path('bondelivraison/delete/<int:blk>/', views.delete_bondeLivraison, name='deleteBL'),
    path('bondelivraison/deleteall/', views.deleteall_bondeLivraison, name='deleteAllBL'),
    path('bondelivraison/add/', views.add_bondeLivraison, name='addBL'),    
    path('bondelivraison/edit/<int:blk>/', views.edit_bondeLivraison, name='editBL'),

    # facture
    path('facture/', views.facture, name='facture'),
    path('facture/delete/<int:fk>/', views.delete_facture, name='deleteF'),
    path('facture/deleteall/', views.deleteall_facture, name='deleteAllF'),
    path('facture/add/', views.add_facture, name='addF'),
    path('facture/edit/<int:fk>/', views.edit_facture, name='editF'),
    
    # reglement
    path('reglement/', views.reglement, name='reglement'),
    path('reglement/payer/<int:rk>/', views.payer_reglement, name='payerR'),

    # stock
    path('stock/', views.stock, name='stock'), 

    #vente
    path('vente/', views.vente, name='vente'),
    path('vente/add/', views.add_vente, name='addV'),
    path('vente/edit/<int:vk>/', views.edit_vente, name='editV'),
    path('vente/delete/<int:vk>/', views.delete_vente, name='deleteV'),
    path('vente/deleteall/', views.deleteall_vente, name='deleteAllV'),


    #paiement credit
    path('paiementcredit/', views.paiementCredit, name='paiementcredit'),
    path('paiementcredit/payer/<int:pck>', views.payer_paiementCredit, name='payerPC'),

    #analyse
    path('analyse/achat/', views.analyse_achat, name='analyse_achat'),
    path('analyse/vente/', views.analyse_vente, name='analyse_vente'),

    path(r'(?<path>.*', views.reglement, name='reglement'),

]
