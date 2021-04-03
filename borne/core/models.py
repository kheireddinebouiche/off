from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone

# Create your models here.


ITEM_TYPE = {

    ('sau','Sauce'),
    ('sup','Suppléments'),
    ('boi','Boisson'),
    ('pat', 'Pate'),
    ('gar', 'garniture'),
    ('san','Sandwich'),
    ('des','Dessert'),
    ('for', 'Formule'),
}

ETAT_COM = {

    ('ann','Annulé'),
    ('arc','Archivé'),
    ('fin', 'Finaliser'),
    ('val', 'Validé'),
    ('enc', 'En cours'),
   
}

TYPE_CONSO= {
    ('emp', 'Emporter'),
    ('srp', 'Sur place'),
}

MODE_CONSOMMATION = {
    ('emp', 'Emporter'),
    ('srp','Sur place'),
}


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    num_identification = models.CharField(max_length=40, null=True,blank=True)
    adresse = models.CharField(max_length=200, null=True,blank=True)
    num_tel = models.IntegerField(null=True,blank=True)
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    code_access = models.CharField(max_length=1000, null=True, blank=True)


    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.num_identification)
        super(Profile, self).save(*args, **kwargs)


def increment_menu_id_number():
        dernier_menu = Menu.objects.all().order_by('id').last()
        if not dernier_menu:
            return 'menu/' + '1'

        identifiant = dernier_menu.identifiant
        item_menu_nb = int(identifiant.split('menu/')[-1])
        n_item_menu_nb = item_menu_nb + 1
        n_item_menu_id = 'menu/' + str(n_item_menu_nb)
        return n_item_menu_id


class Menu(models.Model):

    identifiant = models.CharField(max_length=1000, default=increment_menu_id_number, null=True, blank=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    designation = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    sauce = models.BooleanField(null=True, blank=True)
    pate = models.BooleanField(null=True, blank=True)
    garniture = models.BooleanField(null=True, blank=True)
    

    slug = models.SlugField(max_length=100, null=True, blank=True)

    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.identifiant)
        super(Menu, self).save(*args, **kwargs)

    def __str__(self):
        return self.designation

    def get_url(self):
        return reverse('core:get_url', kwargs={
            'slug' : self.slug
        })

    def go_next_step(self):
        return reverse("core:view_menu", kwargs={
            'slug': self.slug
        })
    


def increment_item_id_number():
        dernier_item = Item.objects.all().order_by('id').last()
        if not dernier_item:
            return 'item/' + '1'

        num_item = dernier_item.num_item
        item_menu_nb = int(num_item.split('item/')[-1])
        n_item_menu_nb = item_menu_nb + 1
        n_item_menu_id = 'item/' + str(n_item_menu_nb)
        return n_item_menu_id


class Item(models.Model):

    num_item = models.CharField(max_length=1000, default=increment_item_id_number, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='Menu', null=True, blank=True)

    designation = models.CharField(max_length=100, null=True, blank=True)

    prix = models.FloatField(blank=True, null=True)
    prix_promo = models.FloatField(blank=True, null=True)
    
    min_commande = models.IntegerField(blank=True, null=True)
    max_commande = models.IntegerField(blank=True, null=True)

    image = models.ImageField(null=True, blank=True)

    type_item = models.CharField(max_length=3, choices=ITEM_TYPE, null=True, blank=True)

    is_formule= models.BooleanField(default=False)

    slug = models.SlugField(max_length=100, null=True, blank=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.num_item)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.designation

    def get_add_to_cart_url(self):
        return reverse("core:add_to_cart", kwargs={
            'slug': self.slug
        })

    def remove_from_cart(self):
        return reverse("core:remove_from_cart", kwargs={
            'slug': self.slug
        })

    def get_add_to_pan(self):
        return reverse('core:add_to_pan', kwargs={
            'slug' : self.slug
        })

    def get_add_garniture(self):
        return reverse('core:add_garniture', kwargs={
            'slug' : self.slug
        })

    def get_add_pate(self):
        return reverse('core:add_pate', kwargs={
            'slug' : self.slug
        })

    def get_add_sauce(self):
        return reverse('core:add_sauce', kwargs={
            'slug' : self.slug
        })

    def remove_single_item(self):
        return reverse("core:remove_single_item_from_cart", kwargs={
            'slug': self.slug
        })

    


def increment_order_id_number():
        derniere_commande = OrderItem.objects.all().order_by('id').last()
        if not derniere_commande:
            return 'commande/' + '1'

        num_commande = derniere_commande.num_commande
        item_menu_nb = int(num_commande.split('commande/')[-1])
        n_item_menu_nb = item_menu_nb + 1
        n_item_menu_id = 'commande/' + str(n_item_menu_nb)
        return n_item_menu_id



class OrderItem(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_commande = models.CharField(max_length=1000, default=increment_order_id_number, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    date_de_demande = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, null=True, blank=True) 

    ref_menu = models.CharField(max_length=1000, null=True, blank=True) 

    prix_unitaire = models.FloatField(default=0)
    montant_total = models.FloatField(default=0)

    etat = models.CharField(max_length=3 ,null=True, blank=True, choices=ETAT_COM)


    def __str__(self):
        return self.item.designation

    def save(self, *args, **kwargs):
        self.slug = slugify(self.num_commande)
        self.montant_total = self.quantity * self.prix_unitaire
        super(OrderItem, self).save(*args, **kwargs)

    def get_total_item_price(self):
        return self.quantity * self.item.prix

    def get_final_price(self):
        return self.get_total_item_price()


def increment_order_id():
        dernier_order = Order.objects.all().order_by('id').last()
        if not dernier_order:
            return 'Order/' + '1'

        num_order = dernier_order.num_order
        item_order_nb = int(num_order.split('Order/')[-1])
        n_item_order_nb = item_order_nb + 1
        n_item_order_id = 'Order/' + str(n_item_order_nb)
        return n_item_order_id

class Order(models.Model):

    num_order= models.CharField(max_length=1000, default=increment_order_id, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    not_orderd = models.BooleanField(default=True)
    etat = models.CharField(max_length=3, null=True, blank=True, choices=ETAT_COM)
    montant = models.FloatField(default=0)
    mode_consommation = models.CharField(max_length=100, null=True, blank=True, choices=MODE_CONSOMMATION)
    ref_menu = models.CharField(max_length=3, choices=ITEM_TYPE, null=True, blank=True)

    step = models.CharField(max_length=3000, null=True, blank=True)

    def __str__(self):
        return self.user.username


    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.det_tot()
        return total


class ModeConso(models.Model):
    type_conso = models.CharField(max_length=3, choices=TYPE_CONSO, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.type_conso)
        super(ModeConso, self).save(*args, **kwargs)

    def __str__(self):
        return self.type_conso

    def get_url(self):
        return reverse("core:set_mode_conso", kwargs={
            'slug': self.slug
        })


