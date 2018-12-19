from rest_framework import serializers


from .models import HostScanInifo





class HostScanInfoSerializers(serializers.ModelSerializer):
    ip = serializers.IPAddressField(protocol='both',read_only=True)
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    login_port = serializers.CharField(read_only=True)
    login_user = serializers.CharField(read_only=True)
    login_passwd = serializers.CharField(read_only=True)
    login_status = serializers.IntegerField(read_only=True,max_value=1, min_value=0,default=0)


    class Meta:
        model = HostScanInifo
        fields = "__all__"


    def create(self, validated_data):
        print (validated_data)
        scanhost = HostScanInifo(
            ip="10.210.23.10",
            login_port="22",
            login_passwd="123456",
            login_status="1",
            login_user="admin"
        )
        scanhost.save()
        return scanhost