"""Badge admin configuration."""

from django.contrib import admin

from apps.nest.models.badge import BadgeType, UserBadge


@admin.register(BadgeType)
class BadgeTypeAdmin(admin.ModelAdmin):
    """Admin for BadgeType model."""

    list_display = (
        "name",
        "description",
        "icon",
        "color",
        "is_active",
        "nest_created_at",
        "nest_updated_at",
    )
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    ordering = ("name",)

    fieldsets = (
        ("Basic Information", {"fields": ("name", "description", "is_active")}),
        (
            "Appearance",
            {
                "fields": ("icon", "color"),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("nest_created_at", "nest_updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = ("nest_created_at", "nest_updated_at")


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    """Admin for UserBadge model."""

    list_display = (
        "user",
        "badge_type",
        "earned_at",
        "reason",
        "nest_created_at",
    )
    list_filter = (
        "badge_type",
        "earned_at",
    )
    search_fields = (
        "user__login",
        "user__name",
        "badge_type__name",
        "reason",
    )
    ordering = ("-earned_at",)

    autocomplete_fields = ("user", "badge_type")

    fieldsets = (
        ("Badge Information", {"fields": ("user", "badge_type", "earned_at", "reason")}),
        (
            "Metadata",
            {
                "fields": ("metadata",),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("nest_created_at", "nest_updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = ("earned_at", "nest_created_at", "nest_updated_at")

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related("user", "badge_type")
