from django.contrib import admin
from django.utils.html import linebreaks
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class ComplianceAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'description',
        'abbrv',
        'is_active',
        'is_trademarked',
        'compliance_type',
        'account',
        'keywords',
        'desc_alt',
        'desc_form',
    )
    list_filter = ('is_active', 'is_trademarked', 'compliance_type')
    search_fields = ('name',)


class ComplianceTypeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'description',
        'is_active',
        'account',
        'desc_alt',
        'desc_form',
    )
    search_fields = ('name',)


class ComplianceVersionAdmin(admin.ModelAdmin):

    list_display = ('id', 'compliance', 'version_number', 'year')
    list_filter = ('compliance',)


class ComplianceRequirementAdmin(admin.ModelAdmin):

    list_display = (
        'compliance_version',
        'cid',
        'family',
        'admin_desc',
        'admin_requirement',
        'admin_testing',
        'admin_guidance',
        'admin_recommendation',
        'admin_compensating_control',
    )
    list_filter = ('compliance_version', 'family', 'priority', 'cid', 'dept')
    search_fields = ('cid', 'family', 'keywords', 'testing')

    def get_ordering(self, request):
        return [('sort_order')]

    def admin_desc(self, obj):
        return linebreaks(obj.desc)
    admin_desc.allow_tags = True
    admin_desc.short_description = 'Description'

    def admin_requirement(self, obj):
        return linebreaks(obj.requirement)
    admin_requirement.allow_tags = True
    admin_requirement.short_description = 'Requirement'

    def admin_testing(self, obj):
        return linebreaks(obj.testing)
    admin_testing.allow_tags = True
    admin_testing.short_description = 'Testing'

    def admin_guidance(self, obj):
        return linebreaks(obj.guidance)
    admin_guidance.allow_tags = True
    admin_guidance.short_description = 'Guidance'

    def admin_scope(self, obj):
        return linebreaks(obj.scope)
    admin_scope.allow_tags = True
    admin_scope.short_description = 'Scoping'

    def admin_recommendation(self, obj):
        return linebreaks(obj.recommendation)
    admin_recommendation.allow_tags = True
    admin_recommendation.short_description = 'Recommendation'

    def admin_compensating_control(self, obj):
        return linebreaks(obj.compensating_control)
    admin_compensating_control.allow_tags = True
    admin_compensating_control.short_description = 'Compensating Controls'


class KillChainAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'description',
        'sort_order',
        'keywords',
        'desc_alt',
        'desc_form',
    )
    search_fields = ('name',)


class NaicsAdmin(admin.ModelAdmin):

    list_display = ('id', 'version', 'code', 'title', 'level')


class PyramidofPainAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'description',
        'abbrv',
        'sort_order',
        'keywords',
        'desc_alt',
        'desc_form',
    )
    search_fields = ('name',)
