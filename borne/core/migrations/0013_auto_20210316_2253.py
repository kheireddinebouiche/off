# Generated by Django 3.0 on 2021-03-16 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20210316_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='type_item',
            field=models.CharField(blank=True, choices=[('pat', 'Pate'), ('sau', 'Sauce'), ('sup', 'Suppléments'), ('for', 'Formule'), ('boi', 'Boisson'), ('san', 'Sandwich'), ('gar', 'garniture'), ('des', 'Dessert')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='etat',
            field=models.CharField(blank=True, choices=[('arc', 'Archivé'), ('enc', 'En cours'), ('val', 'Validé'), ('ann', 'Annulé'), ('fin', 'Finaliser')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='ref_menu',
            field=models.CharField(blank=True, choices=[('pat', 'Pate'), ('sau', 'Sauce'), ('sup', 'Suppléments'), ('for', 'Formule'), ('boi', 'Boisson'), ('san', 'Sandwich'), ('gar', 'garniture'), ('des', 'Dessert')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='etat',
            field=models.CharField(blank=True, choices=[('arc', 'Archivé'), ('enc', 'En cours'), ('val', 'Validé'), ('ann', 'Annulé'), ('fin', 'Finaliser')], max_length=3, null=True),
        ),
    ]
