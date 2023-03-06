# Generated by Django 4.1.4 on 2023-03-04 15:11

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email address')),
                ('otp', models.CharField(blank=True, max_length=20, null=True)),
                ('email_token', models.CharField(max_length=200)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', models.BigIntegerField(blank=True, null=True, verbose_name=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, default=None, max_length=75, null=True)),
                ('zip_code', models.CharField(blank=True, default=None, max_length=75, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('available_from', models.TimeField(blank=True, null=True)),
                ('available_to', models.TimeField(blank=True, null=True)),
                ('profile_image', models.ImageField(blank=True, default=None, null=True, upload_to='Avatar')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', api.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='States',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_name', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'State',
                'verbose_name_plural': 'States',
            },
        ),
        migrations.CreateModel(
            name='WeekDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=50, verbose_name='Day')),
                ('slug_name', models.CharField(max_length=50, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Week Day',
                'verbose_name_plural': 'Week Days',
            },
        ),
        migrations.CreateModel(
            name='BilingInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, default=None, max_length=75, null=True)),
                ('zip_code', models.CharField(blank=True, default=None, max_length=75, null=True)),
                ('state_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.states', verbose_name='User State')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='off_weekdays',
            field=models.ManyToManyField(to='api.weekdays'),
        ),
        migrations.AddField(
            model_name='user',
            name='state_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.states', verbose_name='User State'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
