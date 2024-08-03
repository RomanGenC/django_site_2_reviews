from django.contrib import admin
from .models import Review, Recipient, Specialty
from django.db import models
from django import forms


@admin.register(Review)  # #efefef #F0F8FF
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'recipient',
        'original_review',
        'modified_review',
        'time_create',
        'time_update',
        'is_published',
        'user',
        'user_ip'
    )
    list_filter = ('time_create',)
    search_fields = ['doctor', 'original_review', 'modified_review']
    readonly_fields = ('time_create', 'original_review')
    autocomplete_fields = ('recipient',)
    list_per_page = 10
    formfield_overrides = {
        models.CharField: {'widget': forms.Textarea(
            attrs={'rows': 10, 'cols': 40}
        )},
    }

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('recipient', 'user')


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'second_name', 'last_name', 'description', 'experience', 'photo')
    list_filter = ('second_name',)
    search_fields = ('first_name', 'second_name', 'last_name')
    list_per_page = 10


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ('title',)
    list_per_page = 10
