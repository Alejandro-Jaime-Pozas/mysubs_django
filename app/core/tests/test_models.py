"""
Tests for models.
"""
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.forms.models import model_to_dict

from core.models import (
    Company,
    # LinkedBank,
    # BankAccount,
    # Transaction,
    # Application,
    # Subscription,
    # Tag,
)


def create_user():
    """Create a user for tests."""
    user = get_user_model().objects.create_user(
        email='test@example.com',
        password='testpass123'
    )
    return user


class ModelTests(TestCase):
    """Test models."""

    # USER TESTS

    # test base success case user created and is active
    def test_create_user_with_email_successful(self):
        """ Test creating a user with an email is successful,
            and hashed password is correct.
        """
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password), password)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    # email must be normalized
    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        # domains must be lowercase
        sample_emails = [
            ('test1@EXAMPLE.com', 'test1@example.com'),
            ('Test2@Example.com', 'Test2@example.com'),
            ('TEST3@EXAMPLE.com', 'TEST3@example.com'),
            ('test4@example.COM', 'test4@example.com'),
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'testpass123')

            self.assertEqual(user.email, expected)

    # email must be valid
    def test_email_not_valid(self):
        """Test user email input is not valid."""
        sample_bad_emails = [
            '',
            'test_string',
            'test_no_domain@',
            'test_no_at_symbol.com',
            '@test_no_input_before_at.com',
        ]
        for email in sample_bad_emails:
            # user should NOT be created with invalid email
            with self.assertRaises(ValidationError):
                get_user_model().objects.create_user(
                    email=email,
                    password='testpass123'
                )

    # email must be unique
    def test_email_must_be_unique(self):
        """Test that checks if email is unique by creating email duplicate."""
        user1 = create_user()
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                email='test@example.com',
                password='testpass456'
            )

    # optional password
    def test_password_is_optional(self):
        """Test the password is optional field."""
        email='test@example.com'
        password=None
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertFalse(user.check_password(password))

    # minimum password length should be 8 chars
    def test_minimum_password_length(self):
        """Test the minimum password length is 8 chars."""
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                email='test@example.com',
                password='a234567'
            )

    # if super user check True is_active and is_superuser and is_staff
    def test_create_superuser(self):
        """Test creating a superuser is successfull and is_active,
        is_superuser both True."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'testpass123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)

    def test_user_extra_fields_raise_type_error(self):
        """Test extra fields are accepted as params in UserManager
        but raise type error in user creation model
        (since fields not set in user model)."""
        with self.assertRaises(TypeError):
            get_user_model().objects.create_user(
                email='test@example.com',
                extra_field_1=500,
                extra_field_2=['a','b']
            )


    # COMPANY
    company_name = 'test_company'
    company_domain = 'example.com'

    # create company is successful
    def test_create_company_successful(self):
        """Test creating a company is successful."""
        company = Company.objects.create(
            name=self.company_name,
            domain=self.company_domain
        )
        self.assertEqual(company.name, self.company_name)
        self.assertEqual(company.domain, self.company_domain)

    # name must be filled out
    def test_name_not_null(self):
        """Test that name field is not null."""
        with self.assertRaises(IntegrityError):
            company = Company.objects.create(
                name=None,
                domain=self.company_domain
            )

    # domain must be filled out
    def test_domain_not_null(self):
        """Test the domain field is not null."""
        with self.assertRaises(IntegrityError):
            Company.objects.create(
                name=self.company_name,
                domain=None
            )

    # domain must be unique
    def test_domain_is_unique(self):
        """Test the company domain is unique."""
        company = Company.objects.create(
            name=self.company_name,
            domain=self.company_domain
        )
        with self.assertRaises(IntegrityError):
            Company.objects.create(
                name='second company',
                domain=self.company_domain
            )


    # LINKED_BANK

    # # create LinkedBank is successful
    # def test_create_linked_bank_successful(self):
    #     """Test creating a linked bank account (plaid item) is successful
    #     and that the bank's web portal is active."""
    #     name = 'test_linked_bank'
    #     web_portal_url = 'https://www.example.com'
    #     response = self.client.get(web_portal_url)

    #     linked_bank = LinkedBank.objects.create(
    #         name=name,
    #         web_portal_url=web_portal_url,
    #     )

    #     self.assertEqual(linked_bank.name, name)
    #     self.assertEqual(linked_bank.web_portal_url, web_portal_url)

    # def test_create_linked_bank_successful(self):
    #     """Test creating a linked bank account (plaid item) is successful
    #     and that the bank's web portal is active."""
    #     response = self.client.get(web_portal_url)

    #     linked_bank = LinkedBank.objects.create(
    #         name=name,
    #         web_portal_url=web_portal_url,
    #     )
    #     self.assertGreaterEqual(response.status_code, 200)
    #     self.assertLess(response.status_code, 300)

    # BANK_ACCOUNT

    # TRANSACTION

    # APPLICATION

    # SUBSCRIPTION

    # TAG
