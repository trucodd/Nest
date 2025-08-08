"""Nest app badge models."""

from __future__ import annotations

from django.db import models

from apps.common.models import TimestampedModel


class BadgeType(TimestampedModel):
    """Badge type model defining available badge categories."""

    class Meta:
        db_table = "nest_badge_types"
        verbose_name = "Badge Type"
        verbose_name_plural = "Badge Types"
        ordering = ["name"]

    name = models.CharField(
        verbose_name="Name",
        max_length=100,
        unique=True,
        help_text="Badge type name (e.g., 'WASPY Award Winner')",
    )
    description = models.TextField(
        verbose_name="Description",
        blank=True,
        default="",
        help_text="Description of what this badge represents",
    )
    icon = models.CharField(
        verbose_name="Icon",
        max_length=50,
        blank=True,
        default="🏆",
        help_text="Icon class or emoji for the badge",
    )
    color = models.CharField(
        verbose_name="Color",
        max_length=20,
        blank=True,
        default="#FFD700",
        help_text="Badge color (hex code or CSS color name)",
    )
    is_active = models.BooleanField(
        verbose_name="Is Active",
        default=True,
        help_text="Whether this badge type is currently active",
    )

    def __str__(self) -> str:
        """Return string representation of the badge type."""
        return self.name


class UserBadge(TimestampedModel):
    """User badge model representing badges earned by users."""

    class Meta:
        db_table = "nest_user_badges"
        verbose_name = "User Badge"
        verbose_name_plural = "User Badges"
        constraints = [
            models.UniqueConstraint(fields=["user", "badge_type"], name="unique_user_badge_type")
        ]
        indexes = [
            models.Index(fields=["user"], name="nest_user_badge_user_idx"),
            models.Index(fields=["badge_type"], name="nest_user_badge_type_idx"),
            models.Index(fields=["earned_at"], name="nest_user_badge_earned_at_idx"),
        ]
        ordering = ["-earned_at"]

    user = models.ForeignKey(
        "github.User",
        on_delete=models.CASCADE,
        related_name="badges",
        verbose_name="User",
        help_text="The user who earned this badge",
    )
    badge_type = models.ForeignKey(
        BadgeType,
        on_delete=models.CASCADE,
        related_name="user_badges",
        verbose_name="Badge Type",
        help_text="The type of badge earned",
    )
    earned_at = models.DateTimeField(
        verbose_name="Earned At", auto_now_add=True, help_text="When the badge was earned"
    )
    reason = models.TextField(
        verbose_name="Reason",
        blank=True,
        default="",
        help_text="Reason or context for earning this badge",
    )
    metadata = models.JSONField(
        verbose_name="Metadata",
        default=dict,
        blank=True,
        help_text="Additional metadata about the badge (e.g., award details)",
    )

    def __str__(self) -> str:
        """Return string representation of the user badge."""
        return f"{self.user.login} - {self.badge_type.name}"

    @property
    def display_name(self) -> str:
        """Get display name for the badge."""
        return f"{self.badge_type.name} ({self.earned_at.year})"
