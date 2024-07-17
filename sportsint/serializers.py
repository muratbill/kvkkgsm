from rest_framework import serializers
from .models import Formlar
from .models import Onaylar
class KvkkSerializer(serializers.ModelSerializer):
     class Meta:
         model = Formlar
         fields = ('ad','soyad','email','cepno', 'form_id','kaynak','sube')




class NetResponseSerializer(serializers.ModelSerializer):
     class Meta:
         model = Onaylar
         fields = ( 'submitid', 'resultstatus', 'creationdate', 'user_refcode', 'transactionid', 'type', 'source', 'recipient', 'status', 'consentDate', 'recipientType', 'errcode', 'errmsg')

class PostmanCsvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Onaylar
        fields = ('creationdate', 'consentDate', 'recipient', 'recipientType', 'source', 'status', 'transactionid', 'type')


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Onaylar
        fields = ('consentDate', 'type', 'status', 'source')
