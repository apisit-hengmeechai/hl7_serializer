# Generated by Django 2.0.6 on 2018-06-12 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0004_patient_patientaddress_patientcommunication_patientcontact_patientidentifier_patientname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientorganization',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]