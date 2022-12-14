import logging

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from django.contrib.auth.decorators import login_required

from orders import wc_utils


logger = logging.getLogger(__name__)

@login_required
def order_list(request):
    return render(request, 'orders/list.html', {'orders': []})

@login_required
def order_list_json(request):
    client = wc_utils.get_wc_api_client()
    try:
        data = wc_utils.get_orders(client)
    except Exception as exc:
        logger.exception("Something went wrong: %s", exc)
        data = []
    return JsonResponse(data, safe=False)

@login_required
def order_search(request):
    client = wc_utils.get_wc_api_client()
    query_search = request.GET.get("q")
    try:
        data = wc_utils.search_orders(client, query_search)
    except Exception as exc:
        logger.exception("Something went wrong: %s", exc)
        data = []
    return JsonResponse(data, safe=False)

@require_http_methods(["POST"])
@login_required
def reset_order_cache(request):
    wc_utils.reset_cache()
    return JsonResponse({"response": 200}, safe=False)

def order_pdf(request, order_id):
    client = wc_utils.get_wc_api_client()
    order = wc_utils.get_order(client, order_id)

    context = {
        'order': order,
    }
    html = render_to_string("orders/pdf.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"

    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)

    return response


def order_detail(request, order_id):
    client = wc_utils.get_wc_api_client()
    order = wc_utils.get_order(client, order_id)

    context = {
        'order': order,
    }
    return render(request, 'orders/detail.html', context)