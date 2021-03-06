# Generated by Django 3.1.5 on 2021-05-02 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Features',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('src', models.CharField(max_length=32)),
                ('srcport', models.CharField(max_length=32)),
                ('dst', models.CharField(max_length=32)),
                ('dstport', models.CharField(max_length=32)),
                ('timestamp', models.CharField(max_length=32)),
                ('time', models.CharField(max_length=32)),
                ('proto', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='FlowFeature',
            fields=[
                ('flowid', models.AutoField(primary_key=True, serialize=False)),
                ('flowsrc', models.CharField(max_length=32)),
                ('flowsrcport', models.CharField(max_length=32)),
                ('flowdst', models.CharField(max_length=32)),
                ('flowdstport', models.CharField(max_length=32)),
                ('flowproto', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SessionFeatures',
            fields=[
                ('sessionid', models.AutoField(primary_key=True, serialize=False)),
                ('sessionaddr1', models.CharField(max_length=32)),
                ('sessionport1', models.CharField(max_length=32)),
                ('sessionaddr2', models.CharField(max_length=32)),
                ('sessionport2', models.CharField(max_length=32)),
                ('sessionproto', models.CharField(max_length=10)),
            ],
        ),
    ]
