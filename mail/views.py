from django.shortcuts import render

# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def snail_summary(request):
    # Hard-coded demo data for now
    data = {
        "period": "today",
        "total_emails": 42,
        "by_category": {"work": 20, "personal": 15, "promotions": 7},
    }
    return JsonResponse(data)


# class MailUploadView(LoginRequiredMixin, FormView):
#     template_name = "mail/upload.html"
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
