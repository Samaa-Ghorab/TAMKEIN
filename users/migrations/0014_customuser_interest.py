# Generated by Django 5.1.5 on 2025-02-12 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_customuser_disability_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='interest',
            field=models.CharField(choices=[('AI', 'AI'), ('Web development', 'Web development'), ('Network', 'Network'), ('Mobile app development', 'Mobile app development'), ('Data Science', 'Data Science'), ('Data Engineering', 'Data Engineering'), ('Cybersecurity', 'Cybersecurity'), ('Robotics', 'Robotics')], default='AI', max_length=50),
        ),
    ]
