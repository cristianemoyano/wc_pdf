from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

from orders import wc_utils

from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration


def order_list(request):
    return render(request, 'orders/list.html', {'orders': []})


def order_list_json(request):
    client = wc_utils.get_wc_api_client()
    data = wc_utils.get_orders(client)
    return JsonResponse(data, safe=False)


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
