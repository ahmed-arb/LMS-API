"""core admin panel"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.models import User, Librarian


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    """Registers Librarian model to admin panel"""


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Over ride user view in admin panel"""

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
