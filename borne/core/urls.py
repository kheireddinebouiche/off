from django.contrib import admin

from django.urls import path, include
from .views import home, commande, add_to_cart,sauce, roll_back, com,side, remove_from_cart,remove_single_item_from_cart, supplement, boisson, pate, AnnulerCommande, VoirCommande, garniture, ConfirmerCommande, sandwich, view_menu, formule, ModeConsommation, set_mode_conso
from django.conf.urls.static import static


app_name="core"

urlpatterns = [
    
    #page d'accueil de l'application
    path('', home, name="home"),

    #url de redirection vers le menu choisie
    path('commande_step/<slug>',commande, name="commande" ),

    #url de selection des composants du menu
    path('view_menu/<slug>/', view_menu, name="view_menu"),
    path('sandwich/',sandwich, name="sandwich"),
    path('formule/', formule, name="formule"),
    path('garniture/', garniture, name="garniture"),
    path('choix_d_une_sauce/',sauce,name="sauce"),
    path('supplement/', supplement, name="supplement"),
    path('boisson/',boisson,name="boisson"),
    path('pate/', pate, name="pate"),

    #url de gestion des quantités de la commande
    path('add_to_cart/<slug>/', add_to_cart, name="add_to_cart"), 
    path('remove_from_cart/<slug>',remove_from_cart,name="remove_from_cart"),
    path('remove_single_item/<slug>/',remove_single_item_from_cart,name="remove_single_item_from_cart"),

    #url de gestion
    path('roll_back/',roll_back,name="roll_back"),  
    path('com/', com, name="com"),
    path('side/', side, name="side"),

    #url de traitement de la commande.
    path('AnnulerCommande/', AnnulerCommande, name="AnnulerCommande"),
    path('ModeConsommation/', ModeConsommation, name="ModeConsommation"),
    path('set_mode_conso/<slug>/', set_mode_conso, name="set_mode_conso"),
    path('VoirCommande/',VoirCommande,name="VoirCommande"),
    path('ConfirmerCommande/',ConfirmerCommande, name="ConfirmerCommande"),
    
]

