# Generated by Django 2.0 on 2018-01-18 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0006_auto_20180112_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('image_id', models.AutoField(max_length=15, primary_key=True, serialize=False)),
                ('image_path', models.ImageField(blank=True, null=True, upload_to='static/product_images/')),
            ],
        ),
        migrations.RemoveField(
            model_name='product_ad',
            name='phone_no',
        ),
        migrations.AddField(
            model_name='product_ad',
            name='state',
            field=models.CharField(default='Gujarat', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product_ad',
            name='city',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='product_ad',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='static/product_cover_image/'),
        ),
        migrations.AddField(
            model_name='images',
            name='product_ad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bands.Product_Ad'),
        ),
    ]
