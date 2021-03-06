# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Articles(models.Model):
    id_article = models.TextField(primary_key=False, blank=True, null=True)  # This field type is a guess.
    nom_article = models.TextField(blank=True, null=True)  # This field type is a guess.
    prix_article = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    remise_article = models.IntegerField(blank=True, null=True)
    photo1_article = models.TextField(blank=True, null=True)  # This field type is a guess.
    photo2_article = models.TextField(blank=True, null=True)  # This field type is a guess.
    photo3_article = models.TextField(blank=True, null=True)  # This field type is a guess.
    acienprix_article = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    description_article = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = True
        db_table = 'articles'


class Commande(models.Model):
    id_commande = models.TextField(primary_key=False, blank=True, null=True)  # This field type is a guess.
    date = models.DateTimeField(blank=True, null=True)
    numero_commande = models.TextField(blank=True, null=True)  # This field type is a guess.
    article_commande = models.TextField(blank=True, null=True)  # This field type is a guess.
    couleurs_commande = models.TextField(blank=True, null=True)  # This field type is a guess.
    nombre_commande = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = True
        db_table = 'commande'


class Couleurs(models.Model):
    id_couleurs = models.TextField(primary_key=False, blank=True, null=True)  # This field type is a guess.
    nom_couleurs = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = True
        db_table = 'couleurs'
