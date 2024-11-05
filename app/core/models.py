"""
Database models.
"""
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for User."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        validate_email(email)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # this supports adding multiple dbs if needed (best practice)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create, save and return a new superuser."""
        superuser = self.create_user(email, password, **extra_fields)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save(using=self._db)

        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    """User in the db system."""
    email = models.EmailField(max_length=255, unique=True, blank=False)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)  # django built-in; should not be in serializer
    is_staff = models.BooleanField(default=False)  # django built-in; should not be in serializer

    objects = UserManager()  # This assigns UserManager to manage the User model, providing methods to create users and superusers.

    USERNAME_FIELD = 'email'  # This sets the field used for authentication to be the email address instead of the default username.

    def __str__(self) -> str:
        return f'<User {self.id}|{self.email}>'


class Company(models.Model):
    # TODO create the name field based on the domain name from the user's email IF user checks the option for 'company you're using for subsy is the same as your email domain?'; should maybe make the name unique, since there should really only be unique companies...based on unique domains...
    """Company in the db system."""
    name = models.CharField(max_length=255, blank=False)  # in theory this should not allow blank strings as input, therefore no null values will exist in db
    domain = models.CharField(max_length=255, blank=False, unique=True)

    # def __str__(self) -> str:
    #     return f'<Company {self.id}|{self.email}>'


class LinkedBank(models.Model):
    """Linked Bank (plaid item) in the db system."""
    name = models.CharField(max_length=255)
    web_portal_url = models.URLField(max_length=5000)  # maybe a better way to acct for long urls?


class BankAccount(models.Model):
    """Bank account in the db system."""
    name = models.CharField(max_length=255, blank=False)
    routing_number = models.CharField(max_length=9)
    account_number = models.CharField(max_length=17)
    balance = models.DecimalField(max_digits=52, decimal_places=2, default=0)  # this should prob becaome a class property later with @ symbol...since it requires freq updates
    account_type = models.CharField(max_length=255)


class Transaction(models.Model):
    """Transaction (cash in or cash out) in the db system."""
    merchant = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # CHANGE TO BANK INPUT
    amount = models.DecimalField(max_digits=52, decimal_places=2)


class Application(models.Model):
    """
    Software application/platform in the db system.
    i.e. Netflix, Spotify are applications.
    """
    name = models.CharField(max_length=255)
    domain_url = models.URLField(max_length=5000)


class Subscription(models.Model):
    """
    Subscription in the db system. A subscription is a software platform
    of some form that the company subscribes to in a given, possibly
    interrupted time period.
    """
    PAYMENT_PERIOD_CHOICES = [
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('Q', 'Quarterly'),
        ('Y', 'Yearly'),
    ]

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    payment_period = models.CharField(default='monthly', choices=PAYMENT_PERIOD_CHOICES)


class Tag(models.Model):
    """Tag in the db system. Multi-purpose tag for use in grouping/filtering."""
    pass
    # name = models.
