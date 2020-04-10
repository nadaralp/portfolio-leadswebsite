from rest_framework import serializers
from .models import LeadModel

serializers.Serializer

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadModel
        fields = ('name',
                'email',
                'subject',
                'message',
                'isAnswered',
                'referrer',
                'isTestLead')
        
