from rest_framework import serializers
from . models import Record
class RecordSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source = "get_result_status")
    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = ['uid']
        extra_kwargs = {"result_status":{'write_only':True}}
    
    def create(self, validated_data):
        print("create")
        return Record.objects.create(**validated_data)