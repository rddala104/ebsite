# Generated by Django 2.2.2 on 2020-04-09 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    atomic = False 
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ebsite', '0012_cartline'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Commande',
        ),
        migrations.DeleteModel(
            name='Couleurs',
        ),
        migrations.AlterModelOptions(
            name='articles',
            options={},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Commande', 'verbose_name_plural': 'Commandes'},
        ),
        migrations.AlterModelOptions(
            name='orderdetail',
            options={'verbose_name': "Ligne d'une commande", 'verbose_name_plural': 'Lignes de commandes'},
        ),
        migrations.RemoveField(
            model_name='client',
            name='date_crea_client',
        ),
        migrations.RemoveField(
            model_name='client',
            name='email_client',
        ),
        migrations.RemoveField(
            model_name='client',
            name='genre_client',
        ),
        migrations.RemoveField(
            model_name='client',
            name='nom_client',
        ),
        migrations.RemoveField(
            model_name='client',
            name='password_hash_client',
        ),
        migrations.RemoveField(
            model_name='client',
            name='password_salt_client',
        ),
        migrations.RemoveField(
            model_name='client',
            name='prenom_client',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='adress_default_billing',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='adress_default_shipping',
        ),
        migrations.RemoveField(
            model_name='order',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_adress',
        ),
        migrations.AddField(
            model_name='client',
            name='default_invoicing_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='default_invoicing_address', to='ebsite.Contact', verbose_name='Adresse de facturation par défaut'),
        ),
        migrations.AddField(
            model_name='client',
            name='default_shipping_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='default_shipping_address', to='ebsite.Contact', verbose_name='Adresse de livraison par défaut'),
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur associé'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='invoicing_address',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='order_invoicing_address', to='ebsite.Contact', verbose_name='Adresse de facturation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateField(auto_now=True, verbose_name='Date de la commande'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='order_shipping_address', to='ebsite.Contact', verbose_name='Adresse de livraison'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_date',
            field=models.DateField(null=True, verbose_name="Date de l'expédition"),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('W', 'En attente de validation'), ('P', 'Payée'), ('S', 'Expédiée'), ('C', 'Annulée')], default='W', max_length=1, verbose_name='Statut de la commande'),
        ),
        migrations.AddField(
            model_name='order',
            name='stripe_charge_id',
            field=models.CharField(blank=True, max_length=30, verbose_name='Identifiant de transaction Stripe'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='product_unit_price',
            field=models.FloatField(default=0, verbose_name='Prix unitaire du produit'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebsite.Client', verbose_name='Client ayant passé commande'),
        ),
        migrations.AlterModelTable(
            name='articles',
            table=None,
        ),
    ]
