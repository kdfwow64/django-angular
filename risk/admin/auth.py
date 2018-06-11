"""Auth Admin."""
from django.contrib import admin
from risk.models.auth import AccountMembership, DefaultRoleGrant, UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class UserProfileInline(admin.StackedInline):

    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'


class AccountMembershipInline(admin.TabularInline):

    model = AccountMembership
    extra = 1


class DefaultRoleGrantInline(admin.TabularInline):

    model = DefaultRoleGrant
    extra = 1


class UserAdmin(BaseUserAdmin):
    """Define a new User admin."""

    inlines = (UserProfileInline, )

    fieldsets = (
        ('Login Info', {'fields': ('email', 'password',)}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (('Management Detail'), {
         'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'is_staff', 'is_superuser',),
        }),
    )
    list_display = (
        'id',
        'email',
        'full_name',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_created',
        'last_login',
    )
    search_fields = (
        'full_name',
        'email',
        'id',
    )
    ordering = (
        'email',
    )

    def get_readonly_fields(self, request, obj=None):
        """Get readonly fields of model."""
        return self.readonly_fields + ('date_joined', 'last_login')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = (
#         'title',
#         'phone',
#         'is_verified',
#         'bkof_notes',
#         'due_date_reminder',
#     )
#     list_filter = (
#         'is_reputable',
#         'phone',
#     )


class AccountAdmin(admin.ModelAdmin):
    inlines = (AccountMembershipInline,)
    list_display = (
        'id',
        'name',
        'billing_toggle',
        'billing_poc',
        'billing_phone',
        'billing_email',
        'renewal_reminder',
        'bkof_notes',
        'renewal_ext',
        'strong_auth',
        'is_active',
        'is_reputable',
        'date_deactivated',
        'date_created',
        'date_deleted',
        'date_last_paid',
        'billing_confirmation_code',
        'account_type',
        'owned_by',
        'created_by',
        'deleted_by',
        'deactivated_by',
    )
    list_filter = (
        'is_active',
        'is_reputable',
        'date_deactivated',
        'date_created',
        'date_deleted',
        'date_last_paid',
        'account_type',
        'created_by',
        'deleted_by',
        'deactivated_by',
    )


class AccountTypeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'desc',
        'annual_cost',
        'max_user',
        'max_company',
        'max_company_locations',
        'max_company_asset',
        'max_company_control',
        'max_company_resources',
        'max_register_entries',
        'sort_order',
    )
    search_fields = ('name',)


class UserAccessAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'date_created',
        'date_modified',
        'created_by',
        'modified_by',
        'user',
        'userrole',
        'company',
        'account',
    )
    list_filter = (
        'date_created',
        'date_modified',
        'created_by',
        'modified_by',
        'user',
        'userrole',
        'company',
        'account',
    )


class AuthenticationTypeAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'desc',)
    search_fields = ('name',)

'''
class UserLevelAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'desc')
    search_fields = ('name',)
'''


class UserRoleAdmin(admin.ModelAdmin):

    inlines = (DefaultRoleGrantInline,)
    list_display = ('id', 'name', 'desc')
    search_fields = ('name',)


class UserGrantAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'desc')
    search_fields = ('name',)

'''
class UserRoleGrantAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'desc', 'user_role', 'grant')
    list_filter = ('user_role', 'grant')
    search_fields = ('name',)
'''


class RoleTrackingAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'modifed_date',
        'user_role_from',
        'user_role_to',
        'company',
        'modified_by',
        'user',
    )
    list_filter = ('modifed_date', 'company', 'modified_by', 'user')
