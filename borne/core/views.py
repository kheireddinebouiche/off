from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Menu, Item, OrderItem, Order, ModeConso 
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

# Create your views here.

#vue de connexion au panneau de contrôle 
@login_required
def connect(request):
    pass

@login_required
def com(request):
    return render(request, "Front/com.html")

@login_required
def side(request):
    return render(request,'Front/side.html')

@login_required
def home(request):
    menu = Menu.objects.filter(user=request.user)
    context = {
        'menu' : menu,
    }
    return render(request,'Front/index.html', context)


@login_required
def view_menu(request, slug):

    menu = get_object_or_404(Menu, slug=slug)

    if (menu.designation == 'Sandwich'):
        return redirect('core:sandwich')

    else:

        if (menu.designation == 'FORMULE'):
            return redirect('core:formule')
        else:
            if(menu.designation == 'BOISSONS'):
                return redirect('core:boisson')
   
            else:

                return redirect('core:home')

@login_required
def formule(request):

    item = Item.objects.filter(user=request.user, type_item='for')
    
    try:
        order = Order.objects.get(user=request.user, ordered=False, etat='enc')
        context = {
            'item' : item,
            'order' : order,
        }
        return render(request, 'Front/formule.html', context)

    except ObjectDoesNotExist:

   
        context = {
            'item' : item,
        }
        return render(request, 'Front/formule.html', context)




@login_required
def sandwich(request):

    item = Item.objects.filter(user=request.user, type_item='san')

    try:
        order = Order.objects.get(user=request.user, ordered=False, etat='enc')
        context = {
            'item' : item,
            'order' : order,
        }
        return render(request, 'Front/sandwich.html', context)

    except ObjectDoesNotExist:

   
        context = {
            'item' : item,
        }
        return render(request, 'Front/sandwich.html', context)

    



@login_required
def commande(request,slug):
    menu = get_object_or_404(Menu, slug=slug)

    if (menu.designation == "BOISSONS"):

        item = Item.objects.filter(user=request.user, menu = menu).exclude(type_item="sau").exclude(type_item="sup").exclude(type_item="pat")
        try:
            order = Order.objects.get(user=request.user, ordered=False, etat='enc' )
            context = {
                'item' : item,
                'order' : order,
                'menu' : menu,
            }
            return render(request, 'Front/com.html', context)
        except ObjectDoesNotExist:       
            context = {
                'item' : item,
                'menu' : menu,            
            }
            return render(request, 'Front/com.html', context)

    else :

        item = Item.objects.filter(user=request.user, menu = menu).exclude(type_item="sau").exclude(type_item="boi").exclude(type_item="sup").exclude(type_item="pat").exclude(type_item="gar")
        try:
            order = Order.objects.get(user=request.user, ordered=False, etat='enc' )
            context = {
                'item' : item,
                'order' : order,
                'menu' : menu,
            }
            return render(request, 'Front/com.html', context)
        except ObjectDoesNotExist:       
            context = {
                'item' : item,
                'menu' : menu,            
            }
            return render(request, 'Front/com.html', context)


@login_required
def sauce(request):
    sauce = Item.objects.filter(user=request.user, type_item="sau")
    order_qs = Order.objects.get(user=request.user, ordered=False, etat='enc')
    context = {
        'sauce' : sauce,
        'order_qs' : order_qs,
    }
    return render(request, 'Front/sauce.html', context)

@login_required
def garniture(request):
    garniture = Item.objects.filter(user=request.user, type_item='gar')
    order_qs = Order.objects.get(user=request.user, ordered=False, etat='enc')
  

    try:
        order_qs = Order.objects.get(user=request.user, ordered=False, etat='enc')
        context = {
            'garniture' : garniture,
            'order_qs' : order_qs,

        }
        return render(request, 'Front/garniture.html', context)

    except ObjectDoesNotExist:

        return redirect('core:home')



@login_required
def boisson(request):
    boisson = Item.objects.filter(user=request.user, type_item="boi")
    try:
        order_qs = Order.objects.get(user=request.user, ordered=False, etat='enc')
        context = {
            'boisson' : boisson,
            'order_qs' : order_qs,
        }
        return render(request, "Front/boisson.html", context)

    except ObjectDoesNotExist:

        context = {
            'boisson' : boisson,
        }

        return render(request, "Front/boisson.html", context)



@login_required
def pate(request):
    pate = Item.objects.filter(user=request.user, type_item="pat")
    order_qs = Order.objects.get(user=request.user, ordered=False, etat='enc')
    context = {
        'pate' : pate, 
        'order_qs': order_qs,
    }

    return render(request, 'Front/pate.html', context)


@login_required
def supplement(request):
    supplement = Item.objects.filter(user=request.user, type_item="sup")
    order_qs = Order.objects.get(user=request.user, ordered=False)

    context = {
        'supplement' : supplement,
        'order_qs' : order_qs,

    }

    return render(request, "Front/supplement.html" , context)

@login_required
def desserts(request):
    desserts = Item.objects.filter(user=request.user, type_item="des")
    order_qs = Order.objects.get(user=request.user, ordered=False)

    context = {
        'supplement' : supplement,
        'order_qs' : order_qs,

    }
    return render(request, "Front/supplement.html" , context)

    
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    menu = Menu.objects.filter(designation=item.menu) 

    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
        prix_unitaire=item.prix, 
        etat ='enc',        
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False, etat='enc')


    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():


            if(item.type_item == 'for'):

                return redirect('core:formule')

            else:

                order_item.quantity += 1
                order_item.save()
                    

                if (item.type_item=="sau"):
                    return redirect("core:sauce")

                else:
                    if (item.type_item=='boi'):
                        return redirect("core:boisson")

                    else:
                        if (item.type_item=="pat"):
                            return redirect("core:pate")
                        else:
                            if (item.type_item=="gar"):
                                return redirect("core:garniture")
                            else:
                                if (item.type_item =='for'):
                                    return redirect('core:formule')

                                else:
                                    return redirect("core:sandwich")  

        else:

            if (item.type_item=="sau"):     
                order.items.add(order_item)
                return redirect("core:sauce")
            else:
                if (item.type_item=="boi"):
                    order.items.add(order_item)
                    return redirect('core:boisson')

                else:
                    if (item.type_item=='pat'):
                        order.items.add(order_item)
                        return redirect('core:pate')

                    else:

                        if (item.type_item=="gar"):
                            order.items.add(order_item)
                            return redirect('core:garniture')

                        else:

                            if (item.type_item =='for'):
                                order.items.add(order_item)
                                return redirect('core:formule')

                            else:

                                order.items.add(order_item)
                                return redirect("core:sandwich")
            
    else:

        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date, etat='enc', ref_menu=item.type_item)
        order.items.add(order_item)

        if (item.type_item == 'san'):
            return redirect("core:sandwich")
        else:
            if (item.type_item == 'for'):
                return redirect('core:formule')
            else:

                if(item.type_item =='boi'):
                    return redirect('core:boisson')
                else:
                    return redirect('core:home')




@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
        etat='enc'
    )
    #menu = Menu.objects.get(designation = item.menu)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user,ordered=False, etat='enc')[0]
            order.items.remove(order_item)
            order_item.delete()

            if (item.type_item=="sau"):
                return redirect("core:sauce")

            else:

                if (item.type_item=='boi'):
                    return redirect("core:boisson")

                else: 

                    if (item.type_item=='gar'):
                        return redirect('core:garniture')
                
                    else:

                        if(item.type_item=='pat'):
                            return redirect('core:pate')
                    
                        else:
                            return redirect("core:commande", slug=menu.slug)
        else:           
            return redirect("omniparc:products", slug=slug)
    else:       
        return redirect("omniparc:products", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
        etat='enc',
    )
    
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False,
                etat='enc',

            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)

            if (item.type_item == "boi"):
                return redirect('core:boisson')
            else:

                if(item.type_item == 'sau'):
                    return redirect('core:sauce')

                else:

                    if(item.type_item == 'pat'):
                        return redirect('core:pate')

                    else:
                        if(item.type_item == 'gar'):
                            return redirect('core:garniture')

                        else:
                            if (item.type_item == 'san'):
                                return redirect('core:sandwich')
                     
        else:          
            return redirect("omniparc:products", slug=slug)

    else:
    
        return redirect("omniparc:product", slug=slug)


@login_required
def AnnulerCommande(request):

    try:
        order = Order.objects.get(user=request.user, ordered=False, etat='enc')
        order.etat = 'ann'

        order_items = order.items.all()
        order_items.update(etat='ann')

        for item in order_items:
            item.save()

        order.save()

        return redirect('core:home')

    except ObjectDoesNotExist:

        return redirect('core:home')


@login_required
def VoirCommande(request):
    order = Order.objects.get(user=request.user, ordered=False, etat='enc')

    context = {

        'order' : order
    }

    return render(request, 'Front/validation.html',context)

@login_required
def ConfirmerCommande(request):
    
    try:
        order = Order.objects.get(user=request.user, ordered=False, etat='enc')
        total = 0

        for item in order.items.all():
            total += item.montant_total    
        
        order.montant = total
        order.save()

        return redirect('core:VoirCommande')

    except ObjectDoesNotExist:

        return redirect('core:home')


@login_required
def roll_back(request):

    order_item = OrderItem.objects.filter(item__user=request.user, ordered=False).first()
    menu = Menu.objects.filter(user=request.user, slug=order_item.slug)
   
    return redirect('core:commande', slug=order_item.ref_menu)



@login_required
def ModeConsommation(request):
    conso  = ModeConso.objects.all()

    context = {
        'conso' : conso,
    }
    return render(request, 'Front/consomation.html', context)


@login_required
def set_mode_conso(request, slug):

    mode = get_object_or_404(ModeConso,slug)
    order = Order.objects.filter(user=user.request, ordered=False, etat= enc)

    order.mode_consommation = mode
    order.save()

    return redirect('core:ConfirmerCommande')



@login_required
def ModePaienment(request):
    pass
