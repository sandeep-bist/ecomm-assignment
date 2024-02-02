import ast
from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    snap=serializers.SerializerMethodField(read_only=True)
    
    def get_snap(self,obj):
        
        images=obj.images.all().values()
        for i in images:
            # c=list(i['image_url'])
            c= ast.literal_eval(i['image_url'])
        return c

    class Meta:
        model = Products
        fields = ("name","category","sub_category","price","snap")
        depth=1