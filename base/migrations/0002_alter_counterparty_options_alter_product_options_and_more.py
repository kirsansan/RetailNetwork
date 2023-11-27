# Generated by Django 4.2.7 on 2023-11-26 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='counterparty',
            options={'ordering': ['pk'], 'verbose_name': 'Counterparty', 'verbose_name_plural': 'Counterpartys'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['supplier', 'pk'], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterField(
            model_name='networknode',
            name='debt',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='debt node-to-node'),
        ),
    ]