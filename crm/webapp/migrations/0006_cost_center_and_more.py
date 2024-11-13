# Generated by Django 5.0.4 on 2024-11-13 00:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_tablenames'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cost_Center',
            fields=[
                ('id_cost_center', models.AutoField(primary_key=True, serialize=False)),
                ('cost_center_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='sociedad',
            old_name='nombre_sociedad',
            new_name='sociedad_name',
        ),
        migrations.AlterField(
            model_name='contract',
            name='cost_center',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.cost_center'),
        ),
        migrations.DeleteModel(
            name='Centro',
        ),
    ]
