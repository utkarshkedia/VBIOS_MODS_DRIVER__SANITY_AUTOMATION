from rest_framework import serializers
from .models import GPU, Test_System

class GPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPU
        fields = ('id','name_of_the_gpu','memory_type','board_name','ROM_name')

class Test_SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test_System
        fields = ('id','hostname','Operating_System','Remark')
