# Generated by Django 2.0.5 on 2019-04-17 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ScenicSpot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excelname', models.CharField(max_length=10, verbose_name='文件名称')),
                ('upload_file', models.FileField(blank=True, null=True, upload_to='uploadexcel/%Y/%m', verbose_name='文件上传案例')),
            ],
            options={
                'verbose_name': '上传控件一览',
                'verbose_name_plural': '上传控件一览',
            },
        ),
    ]
