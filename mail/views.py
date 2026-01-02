from .models import Message
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .tasks import sync_gmail_metadata


@login_required
def snail_summary(request):
    # Hard-coded demo data for now
    data = {
        "period": "today",
        "total_emails": 42,
        "by_category": {"work": 20, "personal": 15, "promotions": 7},
    }
    return JsonResponse(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def trigger_gmail_sync(request):
    """
    API endpoint to trigger Gmail sync for the authenticated user.
    """
    days = request.data.get('days', 7)

    # Queue the Celery task
    task = sync_gmail_metadata.delay(request.user.id, days=days)

    return Response({
        "success": True,
        "message": f"Gmail sync queued for {days} days of history",
        "task_id": task.id
    })

@login_required
@api_view(['GET'])
def fetch_mail_for_date(request):

    owner = request.user
    date_str = request.get("date")

    messages = Message.objects.filter(owner=owner, internal_date=date_str)

    return Response({
        "date": date_str,
        'messages': messages.values()})



# class MailListView(LoginRequiredMixin, ListView):
#     form_class = MailUploadForm
#     success_url = reverse_lazy("mail:list")

#     def form_valid(self, form):
#         mail = form.save(owner=self.request.user)
#         process_mail_ocr.delay(mail.id)
#         return super().form_valid(form)

# from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
# from django.http import HttpResponse

# def mail_search(request):
#     q = request.GET.get("q", "").strip()
#     if not q:
#         return HttpResponse("")
#     qs = (MailItem.objects.filter(owner=request.user)
#           .select_related("ocr")
#           .annotate(search=SearchVector("ocr__text"))
#           .filter(search=SearchQuery(q))[:20])
#     return render(request, "mail/partials/search_results.html", {"items": qs})
