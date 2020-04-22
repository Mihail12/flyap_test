from django.db.models import Max
from django.db.models.functions import ExtractYear, ExtractMonth
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from general.models import Agreement


def get_months_list(agreements_qs, year):
    months = agreements_qs.filter(periods__stop_date__year=year)\
        .annotate(max_period_stop_date=Max('periods__stop_date'))\
        .annotate(month=ExtractMonth('max_period_stop_date'))\
        .values_list('month', flat=True).order_by('month')
    months_qs_list = list(months)
    return [months_qs_list.count(i) for i in range(1, 13)]


class AgreementCalendar(APIView):
    def get(self, request, *args, **kwargs):
        agreements_qs = Agreement.objects.all()
        if request.query_params.get('country'):
            agreements_qs = agreements_qs.filter(company__country_id__in=request.query_params['country'].split(','))
        if request.query_params.get('company'):
            agreements_qs = agreements_qs.filter(company_id__in=request.query_params['company'].split(','))
        if request.query_params.get('negotiator'):
            agreements_qs = agreements_qs.filter(negotiator_id__in=request.query_params['negotiator'].split(','))
        years = agreements_qs.values_list('stop_date__year', flat=True).order_by('stop_date__year').distinct()
        data = {
            year: get_months_list(agreements_qs, year)
            for year in years
        }
        return Response(data, status.HTTP_200_OK)
