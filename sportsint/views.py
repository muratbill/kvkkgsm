# Create your views here.
from django.shortcuts import render
from .forms import ConsentForm
from .forms import ConsentFormWoEmail
from .forms import ConsentFormWoCep
from .forms import ConsentFormWo
from .models import Formlar
from .models import Onaylar
from .serializers import KvkkSerializer
from .serializers import NetResponseSerializer
from .serializers import PostmanCsvSerializer
from .serializers import SearchSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import requests
from urllib3.exceptions import InsecureRequestWarning
import json
from json import JSONEncoder
import datetime
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import status
from django.contrib import messages
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import filters
from urllib.parse import unquote
from django.db.models import Max, F, Q


class KisiList(generics.ListAPIView):
    serializer_class = SearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['recipient']
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Onaylar.objects.values('recipient').annotate(consentDate=Max('consentDate'), type=F('type'))
        queryset2 = Onaylar.objects.values('recipient').annotate(consentDate=Max('consentDate'), type=F('type'),status=F('status'))
        search_param = self.request.query_params.get('search', None)
        if search_param is not None:
            # Apply the filter first
            queryset = queryset.filter(recipient__exact=search_param)
            queryset2 = queryset2.filter(recipient__exact=search_param) 
        # Then, apply slicing
        queryset2 = queryset2[:queryset.count()]
        return queryset2

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        if not queryset.exists():
            return Response({'detail': 'KAYIT BULUNAMADI.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def getData(request):

     if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 50
        uyeler = Formlar.objects.all().order_by('email')
        result_page = paginator.paginate_queryset(uyeler, request)
        uye_serializer = KvkkSerializer(result_page, many=True)
        print(type(uye_serializer))
        return paginator.get_paginated_response(uye_serializer.data)
     elif request.method == 'POST':
        uye_serializer = KvkkSerializer(data=request.data)
        if uye_serializer.is_valid():
          uye_serializer.save()
          return Response(uye_serializer.data,
              status=status.HTTP_201_CREATED)
        return Response(uye_serializer.errors,
          status=status.HTTP_400_BAD_REQUEST)
     else:
        uye_serializer = KvkkSerializer(data=payload)
        if uye_serializer.is_valid():
          return Response(uye_serializer.errors,
              status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
@api_view(['GET', 'POST'])

def getDataResponse(request):

     if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 50
        cevaplar = Formlar.objects.all().order_by('form_id')
        result_page = paginator.paginate_queryset(cevaplar, request)
        cevap_serializer = NetResponseSerializer(result_page, many=True)
        veri = json.dumps(cevap_serializer.data)

        return paginator.get_paginated_response(cevap_serializer.data)

     if request.method == 'POST':
        cevap_serializer = NetResponseSerializer(data=request.data, many=True)
        if cevap_serializer.is_valid():
          cevap_serializer.save()
          return Response(cevap_serializer.data,
              status=status.HTTP_201_CREATED)
        return Response(cevap_serializer.errors,
          status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'POST'])
def getPostmanCsv(request):
    if request.method == 'POST':
        cevap_serializer = PostmanCsvSerializer(data=request.data, many=True)
        if cevap_serializer.is_valid():
          cevap_serializer.save()
          return Response(cevap_serializer.data,
              status=status.HTTP_201_CREATED)
        return Response(cevap_serializer.errors,
          status=status.HTTP_400_BAD_REQUEST)

class DateTimeEncoder(JSONEncoder):
        #Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):

                #return obj.isoformat()
          return obj.strftime("%Y-%m-%d %H:%M:%S")


def contact(request, pk):
    try:
        kim = Formlar.objects.get(pk=pk)
        if kim.cepno == '' and kim.email == '':
          data = {'form_id': kim.form_id, 'ad': kim.ad, 'soyad': kim.soyad, 'iys_sms': kim.iys_sms, 'iys_arama': kim.iys_arama, 'iys_email': kim.iys_email, 'k_veriisleme': kim.k_veriisleme, 'k_veripaylasimi': kim.k_veripaylasimi, 'k_yurtdisi': kim.k_yurtdisi, 'k_aydinlatmaMetin': kim.k_aydinlatmaMetin}
          payload = {}
          payload1 = {}
          payload2 = {}
          payload3 = {}
          if request.method == 'POST':
             POST = request.POST.copy()
             POST['form_id'] = kim.form_id
             POST['ad'] = kim.ad
             POST['soyad'] = kim.soyad
             POST['sube'] = kim.sube
             POST['kaynak'] = kim.kaynak
             POST['yontem'] = kim.kaynak
             filled_form = ConsentFormWo(POST, request.FILES, instance=kim)
             if filled_form.is_valid():
                 filled_form.save()
                 return HttpResponseRedirect("/failed")
             else:
                 return render(request, 'sportsint/contactwo.html', {'contactformwo':form, 'pk': pk,})
          form = ConsentFormWo(initial=data)
          return render(request, 'sportsint/contactwo.html', {'contactformwo':form, 'pk': pk,})

        if kim.cepno and kim.email:  

          data = {'form_id': kim.form_id, 'ad': kim.ad, 'soyad': kim.soyad, 'email': kim.email, 'cepno': kim.cepno, 'iys_sms': kim.iys_sms, 'iys_arama': kim.iys_arama, 'iys_email': kim.iys_email, 'k_veriisleme': kim.k_veriisleme, 'k_veripaylasimi': kim.k_veripaylasimi, 'k_yurtdisi': kim.k_yurtdisi, 'k_aydinlatmaMetin': kim.k_aydinlatmaMetin}
          payload = {}
          payload1 = {}
          payload2 = {}
          payload3 = {}
          if request.method == 'POST':
             POST = request.POST.copy()
             POST['form_id'] = kim.form_id
             POST['ad'] = kim.ad
             POST['soyad'] = kim.soyad
             POST['email'] = kim.email
             POST['cepno'] = kim.cepno
             POST['sube'] = kim.sube
             POST['kaynak'] = kim.kaynak
             POST['yontem'] = kim.kaynak
             filled_form = ConsentForm(POST, request.FILES, instance=kim)
             if filled_form.is_valid():
                 kim.userIp = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('HTTP_X_REAL_IP', '')).split(',')[0].strip()
                 kim.formOnayTarihi = datetime.datetime.now()
                 kim.userOs = request.user_agent.os.family + request.user_agent.os.version_string
                 if request.user_agent.is_pc is True:
                    kim.cihaz = 'PC'
                 if request.user_agent.is_mobile is True:
                    kim.cihaz = request.user_agent.device.family
                 if request.user_agent.is_tablet is True:
                    kim.cihaz = request.user_agent.device.family
                 if request.user_agent.is_bot is True:
                    kim.cihaz = 'BOT' + request.user_agent.device.family
                 kim.browser = request.user_agent.browser.family + request.user_agent.browser.version_string
                 p_url = "https://api.netgsm.com.tr/iys/add"
                 if kim.k_aydinlatmaMetin is False:
                    kim.k_veriisleme = False
                    kim.k_veripaylasimi = False
                    kim.k_yurtdisi = False
                 if kim.k_aydinlatmaMetin is True:
                    kim.k_veriisleme = True
                    kim.k_veripaylasimi = True
                    kim.k_yurtdisi = True
                 if kim.iys_arama is True and kim.iys_sms is False and kim.iys_email is False:
                    payload1 = json.dumps({
                         "header": {
                         "username": '3129115916',
                         "password": '2651Sports@2023',
                         "refid": kim.form_id,
                         "brandCode": "647109"
                         },
                         "body": {
                         "data": [{
                         "type": "ARAMA",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "ONAY",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": BIREYSEL
                         },
                          {
                         "type": "MESAJ",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "RET",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                          {
                         "type": "EPOSTA",
                         "source": kim.kaynak,
                         "recipient": kim.email,
                         "status": "RET",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                         ]}
                        }, cls=DateTimeEncoder)
                 if kim.iys_arama is False and kim.iys_sms is True and kim.iys_email is False:
                    payload1 = json.dumps({
                         "header": {
                         "username": "3129115916",
                         "password": '2651Sports@2023',
                         "refid": kim.form_id,
                         "brandCode": "647109"
                         },
                         "body": {
                         "data": [{
                         "type": "MESAJ",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "ONAY",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                          {
                         "type": "EPOSTA",
                         "source": kim.kaynak,
                         "recipient": kim.email,
                         "status": "RET",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                          {
                         "type": "ARAMA",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "RET",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                         ]}
                        }, cls=DateTimeEncoder)
                 if kim.iys_arama is False and kim.iys_sms is False and kim.iys_email is True:
                    payload1 = json.dumps({
                         "header": {
                         "username": "3129115916",
                         "password": '2651Sports@2023',
                         "refid": kim.form_id,
                         "brandCode": "647109"
                         },
                         "body": {
                         "data": [{
                         "type": "MESAJ",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "ONAY",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                         {
                         "type": "EPOSTA",
                         "source": kim.kaynak,
                         "recipient": kim.email,
                         "status": "ONAY",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"

                         },
                          {
                         "type": "ARAMA",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "RET",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },

                         ]}
                        }, cls=DateTimeEncoder)
                 if kim.iys_arama is True and kim.iys_sms is True and kim.iys_email is True:
                    payload1 = json.dumps({
                         "header": {
                         "username": "3129115916",
                         "password": '2651Sports@2023',
                         "refid": kim.form_id,
                         "brandCode": "647109"
                         },
                         "body": {
                         "data": [{
                         "type": "ARAMA",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "ONAY",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                         {
                         "type": "EPOSTA",
                         "source": kim.kaynak,
                         "recipient": kim.email,
                         "status": "ONAY",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                         {
                         "type": "MESAJ",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "ONAY",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"

                         }

                         ]}
                        }, cls=DateTimeEncoder)
                 if kim.iys_arama is True and kim.iys_sms is True and kim.iys_email is False:
                    payload1 = json.dumps({
                         "header": {
                         "username": "3129115916",
                         "password": '2651Sports@2023',
                         "refid": kim.form_id,
                         "brandCode": "647109"
                         },
                         "body": {
                         "data": [{
                         "type": "ARAMA",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "ONAY",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                         {
                         "type": "MESAJ",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "ONAY",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"

                         },
                          {
                         "type": "EPOSTA",
                         "source": kim.kaynak,
                         "recipient": kim.email,
                         "status": "RET",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },

                         ]}
                        }, cls=DateTimeEncoder)
                 if kim.iys_arama is True and kim.iys_email is True and kim.iys_sms is False:
                    payload1 = json.dumps({
                         "header": {
                         "username": "3129115916",
                         "password": '2651Sports@2023',
                         "refid": kim.form_id,
                         "brandCode": "647109"
                         },
                         "body": {
                         "data": [{
                         "type": "ARAMA",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "ONAY",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                         {
                         "type": "EPOSTA",
                         "source": kim.kaynak,
                         "recipient": kim.email,
                         "status": "ONAY",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL",
                         },
                          {
                         "type": "MESAJ",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "RET",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                         ]}
                         }, cls=DateTimeEncoder)
                 if kim.iys_arama is False and kim.iys_sms is False and kim.iys_email is False:
                    payload1 = json.dumps({
                         "header": {
                         "username": "3129115916",
                         "password": '2651Sports@2023',
                         "refid": kim.form_id,
                         "brandCode": "647109"
                         },
                         "body": {
                         "data": [{
                         "type": "MESAJ",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "RET",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                          {
                         "type": "EPOSTA",
                         "source": kim.kaynak,
                         "recipient": kim.email,
                         "status": "RET",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                          {
                         "type": "ARAMA",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "RET",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                         ]}
                        }, cls=DateTimeEncoder)
                 if len(payload1) > 0:
                    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
                    response = requests.request("POST", p_url, data=payload1, verify=False)
                    print(payload1)
                    print(dict(request.POST.items()))
                    content0 = response.content.decode('utf-8').split(",")[0]
                    content1 = response.content.decode('utf-8').split(",")[1]
                    content2 = response.content.decode('utf-8').split(",")[2]
                    kim.code = content0.split(':')[1].strip('\"')
                    kim.code_error = content1.split(':')[1].strip('\"')
                    print(response.json())
                    if response.status_code != 200:
                       return HttpResponseRedirect("/failed")
                 filled_form.save()
                 messages.success(request, message=kim.ad+" "+kim.soyad, extra_tags=kim.form_id)
                 return HttpResponseRedirect("/thank-you")   
             else:
                 return render(request, 'sportsint/contact.html', {'contactform':form, 'pk': pk,})
          form = ConsentForm(initial=data)
          return render(request, 'sportsint/contact.html', {'contactform':form, 'pk': pk,})

        if kim.cepno and kim.email == '':
          data = {'form_id': kim.form_id, 'ad': kim.ad, 'soyad': kim.soyad, 'cepno': kim.cepno, 'iys_sms': kim.iys_sms, 'iys_arama': kim.iys_arama, 'k_veriisleme': kim.k_veriisleme, 'k_veripaylasimi': kim.k_veripaylasimi, 'k_yurtdisi': kim.k_yurtdisi, 'k_aydinlatmaMetin': kim.k_aydinlatmaMetin}
          payload = {}
          payload1 = {}
          payload2 = {}
          payload3 = {}
          if request.method == 'POST':
             POST = request.POST.copy()
             POST['form_id'] = kim.form_id
             POST['ad'] = kim.ad
             POST['soyad'] = kim.soyad
             POST['cepno'] = kim.cepno
             POST['sube'] = kim.sube
             POST['kaynak'] = kim.kaynak
             POST['yontem'] = kim.kaynak
             filled_form = ConsentFormWoEmail(POST, request.FILES, instance=kim)
             if filled_form.is_valid():
                 kim.userIp = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('HTTP_X_REAL_IP', '')).split(',')[0].strip()
                 kim.formOnayTarihi = datetime.datetime.now()
                 kim.userOs = request.user_agent.os.family + request.user_agent.os.version_string
                 if request.user_agent.is_pc is True:
                    kim.cihaz = 'PC'
                 if request.user_agent.is_mobile is True:
                    kim.cihaz = request.user_agent.device.family
                 if request.user_agent.is_tablet is True:
                    kim.cihaz = request.user_agent.device.family
                 if request.user_agent.is_bot is True:
                    kim.cihaz = 'BOT' + request.user_agent.device.family
                 kim.browser = request.user_agent.browser.family + request.user_agent.browser.version_string
                 p_url = "https://api.netgsm.com.tr/iys/add"
                 if kim.k_aydinlatmaMetin is False:
                    kim.k_veriisleme = False
                    kim.k_veripaylasimi = False
                    kim.k_yurtdisi = False
                 if kim.k_aydinlatmaMetin is True:
                    kim.k_veriisleme = True
                    kim.k_veripaylasimi = True
                    kim.k_yurtdisi = True
                 if kim.iys_arama is False and kim.iys_sms is True:
                  kim.iys_email=None
                  payload1 = json.dumps({
                         "header": {
                         "username": "3129115916",
                         "password": '2651Sports@2023',
                         "refid": kim.form_id,
                         "brandCode": "647109"
                         },
                         "body": {
                         "data": [{
                         "type": "MESAJ",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "ONAY",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                          {
                         "type": "ARAMA",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "RET",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                         ]}
                        }, cls=DateTimeEncoder)
                 if kim.iys_arama is False and kim.iys_sms is False:
                  kim.iys_email=None
                  payload1 = json.dumps({
                         "header": {
                         "username": "3129115916",
                         "password": '2651Sports@2023',
                         "refid": kim.form_id,
                         "brandCode": "647109"
                         },
                         "body": {
                         "data": [{
                         "type": "MESAJ",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "RET",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                          {
                         "type": "ARAMA",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "RET",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                         ]}
                        }, cls=DateTimeEncoder)
                 if kim.iys_arama is True and kim.iys_sms is False:
                  kim.iys_email=None
                  payload1 = json.dumps({
                         "header": {
                         "username": "3129115916",
                         "password": '2651Sports@2023',
                         "refid": kim.form_id,
                         "brandCode": "647109"
                         },
                         "body": {
                         "data": [{
                         "type": "MESAJ",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "RET",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                          {
                         "type": "ARAMA",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "ONAY",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },

                         ]}
                        }, cls=DateTimeEncoder)
                 if kim.iys_arama is True and kim.iys_sms is True:
                  kim.iys_email=None
                  payload1 = json.dumps({
                         "header": {
                         "username": "3129115916",
                         "password": '2651Sports@2023',
                         "refid": kim.form_id,
                         "brandCode": "647109"
                         },
                         "body": {
                         "data": [{
                         "type": "ARAMA",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "ONAY",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                         {
                         "type": "MESAJ",
                         "source": kim.kaynak,
                         "recipient": kim.cepno,
                         "status": "ONAY",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"

                         }

                         ]}
                       }, cls=DateTimeEncoder)
                 if len(payload1) > 0:
                    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
                    response = requests.request("POST", p_url, data=payload1, verify=False)
                    print(payload1)
                    print(dict(request.POST.items()))
                    content0 = response.content.decode('utf-8').split(",")[0]
                    content1 = response.content.decode('utf-8').split(",")[1]
                    content2 = response.content.decode('utf-8').split(",")[2]
                    kim.code = content0.split(':')[1].strip('\"')
                    kim.code_error = content1.split(':')[1].strip('\"')
                    print(response.json())
                    if response.status_code != 200:
                       return HttpResponseRedirect("/failed")
                 filled_form.save()
                 messages.success(request, message=kim.ad+" "+kim.soyad, extra_tags=kim.form_id)
                 return HttpResponseRedirect("/thank-you")
             else:
                 return render(request, 'sportsint/contact_wo_email.html', {'contactformwoemail':form, 'pk': pk,})
          form = ConsentForm(initial=data)
          return render(request, 'sportsint/contact_wo_email.html', {'contactformwoemail':form, 'pk': pk,})


        if kim.cepno == '' and kim.email:
          data = {'form_id': kim.form_id, 'ad': kim.ad, 'soyad': kim.soyad, 'email': kim.email, 'iys_email': kim.iys_email, 'k_veriisleme': kim.k_veriisleme, 'k_veripaylasimi': kim.k_veripaylasimi, 'k_yurtdisi': kim.k_yurtdisi, 'k_aydinlatmaMetin': kim.k_aydinlatmaMetin}
          payload = {}
          payload1 = {}
          payload2 = {}
          payload3 = {}
          if request.method == 'POST':
             POST = request.POST.copy()
             POST['form_id'] = kim.form_id
             POST['ad'] = kim.ad
             POST['soyad'] = kim.soyad
             POST['email'] = kim.email
             POST['sube'] = kim.sube
             POST['kaynak'] = kim.kaynak
             POST['yontem'] = kim.kaynak
             filled_form = ConsentFormWoCep(POST, request.FILES, instance=kim)
             if filled_form.is_valid():
                 kim.userIp = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('HTTP_X_REAL_IP', '')).split(',')[0].strip()
                 kim.formOnayTarihi = datetime.datetime.now()
                 kim.userOs = request.user_agent.os.family + request.user_agent.os.version_string
                 if request.user_agent.is_pc is True:
                    kim.cihaz = 'PC'
                 if request.user_agent.is_mobile is True:
                    kim.cihaz = request.user_agent.device.family
                 if request.user_agent.is_tablet is True:
                    kim.cihaz = request.user_agent.device.family
                 if request.user_agent.is_bot is True:
                    kim.cihaz = 'BOT' + request.user_agent.device.family
                 kim.browser = request.user_agent.browser.family + request.user_agent.browser.version_string
                 p_url = "https://api.netgsm.com.tr/iys/add"
                 if kim.k_aydinlatmaMetin is False:
                    kim.k_veriisleme = False
                    kim.k_veripaylasimi = False
                    kim.k_yurtdisi = False
                 if kim.k_aydinlatmaMetin is True:
                    kim.k_veriisleme = True
                    kim.k_veripaylasimi = True
                    kim.k_yurtdisi = True
                 if  kim.iys_email is True:
                    kim.iys_sms=None
                    kim.iys_arama=None
                    payload1 = json.dumps({
                         "header": {
                         "username": "3129115916",
                         "password": '2651Sports@2023',
                         "refid": kim.form_id,
                         "brandCode": "647109"
                         },
                         "body": {
                         "data": [{
                         "type": "EPOSTA",
                         "source": kim.kaynak,
                         "recipient": kim.email,
                         "status": "ONAY",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL",
                         },
                         ]}
                         }, cls=DateTimeEncoder)
                 if  kim.iys_email is False:
                    kim.iys_sms=None
                    kim.iys_arama=None
                    payload1 = json.dumps({
                         "header": {
                         "username": "3129115916",
                         "password": '2651Sports@2023',
                         "refid": kim.form_id,
                         "brandCode": "647109"
                         },
                         "body": {
                         "data": [{
                         "type": "EPOSTA",
                         "source": kim.kaynak,
                         "recipient": kim.email,
                         "status": "RET",
                         "consentDate": datetime.datetime.now(),
                         "recipientType": "BIREYSEL"
                         },
                         ]}
                        }, cls=DateTimeEncoder)
                 if len(payload1) > 0:
                    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
                    response = requests.request("POST", p_url, data=payload1, verify=False)
                    print(payload1)
                    print(dict(request.POST.items()))
                    content0 = response.content.decode('utf-8').split(",")[0]
                    content1 = response.content.decode('utf-8').split(",")[1]
                    content2 = response.content.decode('utf-8').split(",")[2]
                    kim.code = content0.split(':')[1].strip('\"')
                    kim.code_error = content1.split(':')[1].strip('\"')
                    print(response.json())
                    if response.status_code != 200:
                       return HttpResponseRedirect("/failed")
                 filled_form.save()
                 messages.success(request, message=kim.ad+" "+kim.soyad, extra_tags=kim.form_id)
                 return HttpResponseRedirect("/thank-you")
             else:
                 return render(request, 'sportsint/contact_wo_cepno.html', {'contactformwocep':form, 'pk': pk,})
          form = ConsentFormWoCep(initial=data)
          return render(request, 'sportsint/contact_wo_cepno.html', {'contactformwocep':form, 'pk': pk,})

    except Formlar.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

def thank_you(request, template_name='sportsint/thank-you.html'):

    return render(request,template_name)

def index(request):
    return render(request, "sportsint/home.html")

def thank_you_nochoice(request, template_name='sportsint/thank-you-nochoice.html'):

    return render(request,template_name)

def failed(request, template_name='sportsint/failed.html'):
    return render(request,template_name)



