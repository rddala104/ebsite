from django.contrib import admin
from django.utils.text import Truncator
from .models import *

class ArticlesAdmin(admin.ModelAdmin):
   list_display   = ('nom_article', 'description_article')##Liste des champs du modèle à afficher dans le tableau
   list_filter    = ('nom_article',)##Liste des champs à partir desquels nous pourrons filtrer les entrées
##   date_hierarchy = 'date'##Permet de filtrer par date de façon intuitive
 ##  ordering       = ('date', )##Tri par défaut du tableau
   search_fields  = ('nom_article', 'description_article')##Configuration du champ de recherche
   def apercu_contenu(self, Articles):
        """ 
        Retourne les 40 premiers caractères du contenu de l'article, 
        suivi de points de suspension si le texte est plus long. 
        """
        return Truncator(Articles.nom_article).chars(40, truncate='...')

    # En-tête de notre colonne
 ##   apercu_contenu.short_description = 'Aperçu du contenu'


class AddressAdmin(admin.ModelAdmin):
    list_display = ('rue', 'codepostal', 'ville', 'client')


class AddressInline(admin.StackedInline):
    model = Contact
    extra = 1


class ClientAdmin(admin.ModelAdmin):
    search_fields = ('user__prenom_contact', 'user__nom_contact', 'user__email')
    inlines = [
        AddressInline,
    ]

class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    readonly_fields = ('total',)
    fields = ()
    extra = 3

    def total(self, instance):
        if instance.id:
            return instance.total
        else:
            return ""


class OrderAdmin(admin.ModelAdmin):
    def total(self, instance):
        return instance.total
    list_display = ('order_date', 'client', 'shipping_address', 'stripe_charge_id', 'total')
    list_filter = ('client',)
    readonly_fields = ('total', 'stripe_charge_id')
    inlines = [
        OrderDetailInline,
    ]
admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Contact, AddressAdmin)
# admin.site.register(Articles, ProductAdmin)
admin.site.register(Order, OrderAdmin)
# Register your models here.
