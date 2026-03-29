from django.contrib import admin
# admin = Django's built-in admin panel at /admin/
# This is a FREE powerful UI to manage your database — no frontend needed

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Django has a built-in UserAdmin for its default User model
# We import it as BaseUserAdmin so our class can inherit from it
# This gives us password change forms, permission panels for FREE

from .models import User
# Import OUR custom User model
# . means "from the same folder (authentication app)"


@admin.register(User)
# @admin.register = decorator that registers User model with admin panel
# Without this line, User table won't appear in /admin/
# This is the same as: admin.site.register(User, UserAdmin)

class UserAdmin(BaseUserAdmin):
    # We inherit BaseUserAdmin to get all default admin features
    # Then we customize what columns and fields to show

    list_display = ('email', 'full_name', 'is_active', 'is_staff', 'created_at')
    # list_display = columns shown in the Users LIST page in admin
    # When you open /admin/authentication/user/ — these are the table columns

    list_filter = ('is_active', 'is_staff')
    # Adds filter sidebar on the right side of admin list
    # You can click "Active: Yes/No" to filter users

    search_fields = ('email', 'full_name')
    # Adds a search box at the top of admin list
    # You can search users by email or name

    ordering = ('-created_at',)
    # - means DESCENDING — newest users shown first
    # Without - it would show oldest users first

    fieldsets = (
        # fieldsets = how fields are GROUPED when you open a user to EDIT
        (None, {'fields': ('email', 'password')}),
        # First section: no title, shows email and password

        ('Personal info', {'fields': ('full_name',)}),
        # Second section titled "Personal info": shows full_name

        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        # Third section titled "Permissions": shows permission fields
    )

    add_fieldsets = (
        # add_fieldsets = fields shown when CREATING a NEW user in admin
        # Different from fieldsets (which is for editing existing users)
        (None, {
            'classes': ('wide',),    # CSS class for wider input boxes
            'fields': ('email', 'full_name', 'password1', 'password2'),
            # password1 = enter password
            # password2 = confirm password (must match)
        }),
    )