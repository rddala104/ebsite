# Generated by Django 2.2.2 on 2019-12-07 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_article', models.TextField(blank=True, null=True)),
                ('nom_article', models.TextField(blank=True, null=True)),
                ('prix_article', models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)),
                ('remise_article', models.IntegerField(blank=True, null=True)),
                ('photo1_article', models.TextField(blank=True, null=True)),
                ('photo2_article', models.TextField(blank=True, null=True)),
                ('photo3_article', models.TextField(blank=True, null=True)),
                ('acienprix_article', models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)),
                ('description_article', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'articles',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_commande', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('numero_commande', models.TextField(blank=True, null=True)),
                ('article_commande', models.TextField(blank=True, null=True)),
                ('couleurs_commande', models.TextField(blank=True, null=True)),
                ('nombre_commande', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'commande',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Couleurs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_couleurs', models.TextField(blank=True, null=True)),
                ('nom_couleurs', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'couleurs',
                'managed': True,
            },
        ),
    ]
