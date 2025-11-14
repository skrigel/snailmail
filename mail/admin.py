from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import GmailSyncState, Message

# If you wired Celery task for syncing:
try:
    from .tasks import sync_gmail_metadata
except Exception:  # Celery not wired yet? keep admin usable.
    sync_gmail_metadata = None


@admin.register(GmailSyncState)
class GmailSyncStateAdmin(admin.ModelAdmin):
    list_display = ("owner", "last_history_id")
    search_fields = ("owner__username", "owner__email", "last_history_id")
    list_select_related = ("owner",)
    actions = ["queue_gmail_resync"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("owner")

    # @admin.display(description="linked_google?")
    # def linked_google(self, obj):
    #     # Lightweight indicator; real check would look at SocialAccount
    #     return bool(obj.last_history_id)  # tweak as you like

    @admin.action(description="Queue Gmail re-sync (last 7 days)")
    def queue_gmail_resync(self, request, queryset):
        if not sync_gmail_metadata:
            self.message_user(
                request,
                "Sync task not available (Celery not configured or task missing).",
                level="warning",
            )
            return
        owners = {state.owner_id for state in queryset}
        for uid in owners:
            sync_gmail_metadata.delay(uid, days=7)
        self.message_user(request, f"Queued re-sync for {len(owners)} user(s).")



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "internal_date",
        "direction",
        "owner",
        "from_to",
        "subject_short",
    )
    list_filter = ("direction",)
    date_hierarchy = "internal_date"
    ordering = ("-internal_date",)
    search_fields = (
        "gmail_id",
        "thread_id",
        "from_email",
        "to_email",
        "subject",
        "snippet",
        "owner__username",
        "owner__email",
    )
    list_select_related = ("owner",)

    readonly_fields = (
        "owner",
        "gmail_id",
        "thread_id",
        "internal_date",
        "from_email",
        "to_email",
        "subject",
        "label_ids",
        "direction",
        "snippet",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="from → to")
    def from_to(self, obj):
        f = (obj.from_email or "").split()[-1]
        t = (obj.to_email or "").split()[-1]
        return f"{f} → {t}"

    @admin.display(description="subject")
    def subject_short(self, obj):
        s = obj.subject or ""
        return s if len(s) <= 80 else s[:77] + "…"