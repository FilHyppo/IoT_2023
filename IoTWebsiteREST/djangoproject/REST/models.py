import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

PARAMS = ['data', 'umidita'] #parametri che ogni misurazione dovrebbe contenere


# Create your models here.
class Igrometro(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    latitudine = models.FloatField()
    longitudine = models.FloatField()
    data_creazione = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    ultima_misurazione = models.JSONField(default=dict, blank=True, null=True)
    misurazioni = models.JSONField(default=list, blank=True, null=True)


    attivo = models.BooleanField(default=False)
    master = models.ForeignKey('MasterIgrometri', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.nome
    
class MasterIgrometri(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    latitudine = models.FloatField()
    longitudine = models.FloatField()
    data_creazione = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    quota = models.FloatField()
    def __str__(self):
        return self.nome
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'indirizzo email è obbligatorio.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

# Override the groups field
    groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                    'granted to each of their groups.'),
        related_name="customuser_set",
        related_query_name="user",
    )

    # Override the user_permissions field
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="customuser_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.email
    