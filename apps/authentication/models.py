import uuid
# uuid = Universally Unique Identifier
# Instead of id = 1, 2, 3 (easy to guess and hack)
# We use id = "a3f8c2d1-4b5e-..." (impossible to guess)
# In real companies, UUIDs are used for security

from django.contrib.auth.models import (
    AbstractBaseUser,   # gives us password hashing, last_login — but NO fields
    BaseUserManager,    # helps Django know HOW to create users
    PermissionsMixin    # gives us is_superuser, groups, permissions
)
from django.db import models
# models = Django's way of creating database tables using Python classes
# Each class = one table in PostgreSQL
# Each field = one column in that table


class UserManager(BaseUserManager):
    # WHY UserManager?
    # Django needs to know HOW to create a user with our custom fields
    # Default Django creates user with username+password
    # We want email+password — so we tell Django our own way

    def create_user(self, email, full_name, password=None):
        # This method runs when someone registers
        # password=None means it's optional at creation time

        if not email:
            raise ValueError("Email is required")
            # raise = throw an error and stop execution
            # In real company APIs, this becomes a 400 Bad Request response

        if not full_name:
            raise ValueError("Full name is required")

        email = self.normalize_email(email)
        # normalize_email converts:
        # "ABHI@GMAIL.COM" → "ABHI@gmail.com"
        # Keeps email consistent in the database
        # Prevents duplicate accounts like Abhi@gmail.com and abhi@gmail.com

        user = self.model(email=email, full_name=full_name)
        # self.model = our User class below
        # This creates a User object in memory — NOT saved to DB yet

        user.set_password(password)
        # VERY IMPORTANT — never store plain text passwords!
        # set_password() converts "admin123" → "$2b$12$randomhashedstring..."
        # Even we (developers) cannot see the real password
        # This is bcrypt hashing — industry standard security

        user.save(using=self._db)
        # NOW it saves to PostgreSQL database
        # using=self._db means use the database defined in settings.py

        return user

    def create_superuser(self, email, full_name, password=None):
        # This runs when you do: python manage.py createsuperuser
        # Superuser = admin who can access /admin panel
        # Regular users CANNOT access /admin

        user = self.create_user(email, full_name, password)
        # First create a normal user using our method above

        user.is_staff = True
        # is_staff = can login to Django admin panel at /admin/

        user.is_superuser = True
        # is_superuser = has ALL permissions — can do everything

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # WHY inherit AbstractBaseUser?
    # It gives us: password field, last_login field, password hashing methods
    # But it does NOT give us email, name etc — we define those ourselves
    
    # WHY inherit PermissionsMixin?
    # It gives us: is_superuser, groups, user_permissions fields
    # Needed for Django admin and role-based access control

    id = models.UUIDField(
        primary_key=True,   # this is the main identifier for each row
        default=uuid.uuid4, # auto-generate a UUID when user is created
        editable=False      # no one can change the ID manually
    )
    # WHY UUID instead of 1,2,3?
    # If id=1,2,3 — hacker can try /api/users/1 /api/users/2 and get all users
    # UUID is random — impossible to guess another user's ID

    email = models.EmailField(unique=True)
    # EmailField = validates that input is a real email format
    # unique=True = no two users can have same email
    # This is our LOGIN FIELD (like username in default Django)

    full_name = models.CharField(max_length=150)
    # CharField = text field with a maximum length
    # max_length=150 = cannot store more than 150 characters

    is_active = models.BooleanField(default=True)
    # True = user account is active, can login
    # False = account is disabled (soft delete — we don't delete users in companies)
    # WHY not delete? — audit trails, compliance, data integrity

    is_staff = models.BooleanField(default=False)
    # False = normal user, cannot access /admin panel
    # True = staff member, can access /admin panel

    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True = automatically saves current time when user is CREATED
    # We never set this manually — Django handles it
    # Used for: "when did this user register?"

    updated_at = models.DateTimeField(auto_now=True)
    # auto_now=True = automatically updates time whenever user record is SAVED
    # Used for: "when was this user's profile last changed?"

    objects = UserManager()
    # Connect our custom manager to this model
    # This is why User.objects.create_user() works

    USERNAME_FIELD = 'email'
    # Tell Django: use EMAIL as the login field
    # Default Django uses 'username' — we changed it to 'email'
    # Now login requires email + password instead of username + password

    REQUIRED_FIELDS = ['full_name']
    # Fields asked when running: python manage.py createsuperuser
    # Email and password are always asked — these are EXTRA required fields

    class Meta:
        db_table = 'users'
        # The actual table name in PostgreSQL will be 'users'
        # Without this, Django names it 'authentication_user' (app_model)
        # Clean table name = better for database queries and readability

    def __str__(self):
        return f"{self.full_name} ({self.email})"
        # __str__ = what shows when you print a User object
        # In Django admin list, each user shows as: "Abhilash (abhi@gmail.com)"
        # Without this, admin shows: "User object (1)" — not helpful!