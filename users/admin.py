from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    # ?????????
    form = UserChangeForm
    add_form = UserCreationForm

    # ???????????
    # ???????UserAdmin???
    list_display = ('email', 'is_admin', 'is_active',)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active',)})
    )

    # add_fieldsets?????ModelAdmin??
    # UserAdmin?????????????get_fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'username', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# ??????User?UserAdmin
admin.site.register(User, UserAdmin)
# ??????????????????Django??????????????admin???Group
admin.site.unregister(Group)


