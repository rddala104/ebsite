from django.db import models
import random
import string
import decimal
from django.contrib.auth.models import User

# Create your models here.


    # def get_absolute_url(self):
    #     return reverse('article:product', kwargs={
    #         'slug': self.slug
    #     })



# class Commande(models.Model):
#     id_commande = models.TextField(primary_key=False, blank=True, null=True)  # This field type is a guess.
#     date = models.DateTimeField(blank=True, null=True)
#     numero_commande = models.TextField(blank=True, null=True)  # This field type is a guess.
#     article_commande = models.TextField(blank=True, null=True)  # This field type is a guess.
#     couleurs_commande = models.TextField(blank=True, null=True)  # This field type is a guess.
#     nombre_commande = models.TextField(blank=True, null=True)  # This field type is a guess.

#     class Meta:
#         managed = True
#         db_table = 'commande'


# class Couleurs(models.Model):
#     id_couleurs = models.TextField(primary_key=False, blank=True, null=True)  # This field type is a guess.
#     nom_couleurs = models.TextField(blank=True, null=True)  # This field type is a guess.

#     class Meta:
#         managed = True
#         db_table = 'couleurs'

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="Utilisateur associé")
    # default_shipping_address = models.ForeignKey("Contact",
    #                                              related_name="default_shipping_address",
    #                                              null=True,
    #                                              on_delete=models.CASCADE,
    #                                              verbose_name="Adresse de livraison par défaut"
    #                                              )
    # default_invoicing_address = models.ForeignKey("Contact",
    #                                               related_name="default_invoicing_address",
    #                                               null=True,
    #                                               on_delete=models.CASCADE,
    #                                               verbose_name="Adresse de facturation par défaut"
    #                                               )

    def __unicode__(self):
        return self.user.username + " (" + self.user.prenom_contact + " " + self.user.nom_contact + ")"

    def addresses(self):
        return Contact.objects.filter(client_id=self.id)

    def orders(self):
        return Order.objects.filter(client_id=self.id).order_by('-id')

    # def __str__(self):
    #     return self.email_client
    
class Contact(models.Model):
    client=models.ForeignKey(Client, on_delete=models.CASCADE)
    prenom_contact=models.CharField(max_length=200)
    nom_contact=models.CharField(max_length=200)
    company=models.CharField(max_length=200)
    rue=models.CharField(max_length=200)
    codepostal=models.CharField(max_length=200)
    pays=models.CharField(max_length=200)
    ville=models.CharField(max_length=200)
    telephone=models.CharField(max_length=200)

    # class Meta:
    #     verbose_name = 'Adresse'
    #     verbose_name_plural = 'Adresses'

    def __unicode__(self):
        return self.prenom_contact + " " + self.nom_contact + " (" + self.rue + ", " + self.codepostal + " " + self.ville + ")"

class Articles(models.Model):
    id_article = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_article = models.TextField(blank=True, null=True)  # This field type is a guess.
    prix_article = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    remise_article = models.IntegerField(blank=True, null=True)
    photo1_article = models.ImageField(upload_to='media/', default = 'media/comingsoon.png')  # This field type is a guess.
    photo2_article = models.ImageField(upload_to='media/', default = 'media/comingsoon.png')  # This field type is a guess.
    photo3_article = models.TextField(blank=True, null=True)  # This field type is a guess.
    acienprix_article = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    description_article = models.TextField(blank=True, null=True)  # This field type is a guess.
    slug = models.SlugField()
   
    def __unicode__(self):
        return self.nom_article
    # class Meta:
    #     managed = True
    #     db_table = 'articles'

    # def __str__(self):
    #     return self.nom_article
class Order(models.Model):
    client = models.ForeignKey(Client,on_delete=models.CASCADE, verbose_name="Client ayant passé commande")
    shipping_address = models.ForeignKey(Contact,
                                         verbose_name="Adresse de livraison",
                                         on_delete=models.CASCADE,
                                         related_name="order_shipping_address"
                                         )
    invoicing_address = models.ForeignKey(Contact,
                                          verbose_name="Adresse de facturation",
                                          on_delete=models.CASCADE,
                                          related_name="order_invoicing_address"
                                          )
    order_date = models.DateField(verbose_name="Date de la commande", auto_now=True)
    shipping_date = models.DateField(verbose_name="Date de l'expédition", null=True)
    WAITING = 'W'
    PAID = 'P'
    SHIPPED = 'S'
    CANCELED = 'C'
    STATUS = (
        (WAITING, 'En attente de validation'),
        (PAID, 'Payée'),
        (SHIPPED, 'Expédiée'),
        (CANCELED, 'Annulée'),
    )
    status = models.CharField(max_length=1, choices=STATUS, default=WAITING, verbose_name="Statut de la commande")
    stripe_charge_id = models.CharField(max_length=30, verbose_name="Identifiant de transaction Stripe", blank=True)

    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'

    @property
    def total(self):
        total = 0
        order_details = OrderDetail.objects.filter(order_id=self.id)
        for order_detail in order_details:
            total += order_detail.total()
        return round(total,2)

    def article_qty(self):
        order_details = OrderDetail.objects.filter(order_id=self.id)
        return len(order_details)

class OrderDetail(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    article=models.ForeignKey(Articles, on_delete=models.CASCADE)
    qty=models.IntegerField(verbose_name="Quantité")
    product_unit_price = models.FloatField(verbose_name="Prix unitaire du produit")
    # vat = models.FloatField(verbose_name="Taux de TVA")

    class Meta:
        verbose_name = 'Ligne d\'une commande'
        verbose_name_plural = 'Lignes de commandes'

    def total_ht(self):
        return round(self.product_unit_price * self.qty, 2)

    # def total_vat(self):
    #     return round(self.product_unit_price * float(self.qty) * self.vat, 2)

    def total(self):
        return round((self.product_unit_price * self.qty))
        #  + (self.product_unit_price * self.qty, 2))

class CartLine(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Articles, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'Ligne d\'un panier client'
        verbose_name_plural = 'Lignes d\'un panier client'
    
    def total_ht(self):
        return round(self.product.prix_article *  decimal.Decimal(float(self.quantity)), 2)

    # def total_vat(self):
    #     return round(self.product.price * float(self.quantity) * self.product.vat.percent, 2)

    def total(self):
        return round((self.product.prix_article *  decimal.Decimal(float(self.quantity))), 2)


class mur(models.Model):
    message = models.TextField(blank=True, null=True)
    pseudo = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.message
