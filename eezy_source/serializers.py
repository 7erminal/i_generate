from rest_framework import serializers
from django.contrib.auth import get_user_model
from eezy_source.models import Receipt, ProcessConfig, Record, FX, SystemUnits, Currency

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    firstName = serializers.CharField(source='first_name', required=False, allow_blank=True)
    lastName = serializers.CharField(source='last_name', required=False, allow_blank=True)
    phoneNumber = serializers.CharField(required=False, allow_blank=True, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'firstName', 'lastName', 'phoneNumber']

    def create(self, validated_data):
        # phoneNumber is accepted for backward compatibility, but Django's default User has no such field.
        validated_data.pop('phoneNumber', None)
        user = User.objects.create_user(
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email')
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class RegisterResponseSerializer(serializers.Serializer):
    statusCode = serializers.IntegerField()
    statusDesc = serializers.CharField()
    result = serializers.CharField()

class LoginResponseSerializer(serializers.Serializer):
    statusCode = serializers.IntegerField()
    statusDesc = serializers.CharField()
    result = serializers.CharField()

class ConfigurationSerializer(serializers.Serializer):
    businessName = serializers.CharField(max_length=100)
    businessPhone = serializers.CharField(max_length=100, required=False, allow_blank=True)
    businessEmail = serializers.CharField(max_length=100, required=False, allow_blank=True)
    businessAddress = serializers.CharField(max_length=100, required=False, allow_blank=True)
    processCode = serializers.CharField(max_length=100)
    sellerShipperDeliveryFee = serializers.FloatField(required=False)
    sellerShipperDeliveryFeeUnit = serializers.CharField(max_length=100, required=False)
    handlingFee = serializers.FloatField(required=False)
    handlingFeeUnit = serializers.CharField(max_length=100, required=False)
    weightUnit = serializers.CharField(max_length=100, required=False)
    shippingMode = serializers.CharField(max_length=100, required=False)
    customRate = serializers.FloatField(required=False)
    customRateUnit = serializers.CharField(max_length=100, required=False)
    shippingMargin = serializers.FloatField(required=False)
    shippingMarginUnit = serializers.CharField(max_length=100, required=False)
    defaultCurrency = serializers.CharField(max_length=100, required=False)

class BusinessSerializer(serializers.Serializer):
    businessName = serializers.CharField(max_length=100)
    businessPhone = serializers.CharField(max_length=100, required=False, allow_blank=True)
    businessEmail = serializers.CharField(max_length=100, required=False, allow_blank=True)
    businessAddress = serializers.CharField(max_length=100, required=False, allow_blank=True)

class ConfigurationSerializerGet(serializers.ModelSerializer):
    business = BusinessSerializer()
    class Meta:
        model = ProcessConfig
        fields = '__all__'
        depth = 1

class ConfigurationResponseSerializer(serializers.Serializer):
    statusCode = serializers.IntegerField()
    statusDesc = serializers.CharField()
    result = ConfigurationSerializerGet()

class ConfigurationsResponseSerializer(serializers.Serializer):
    statusCode = serializers.IntegerField()
    statusDesc = serializers.CharField()
    result = ConfigurationSerializerGet(many=True)

class RecordSerializer(serializers.Serializer):
    itemName = serializers.CharField(max_length=200)
    itemCost = serializers.FloatField(required=False)
    weight = serializers.FloatField(required=False)
    quantity = serializers.IntegerField(required=False)
    deliveryFee = serializers.FloatField(required=False)    

class RecordSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'
        depth = 1

class ReceiptSerializer(serializers.Serializer):
    receiptCode = serializers.CharField(max_length=100)
    receiptName = serializers.CharField(max_length=100, required=False)
    createdBy = serializers.CharField(max_length=100, required=False)
    items = RecordSerializer(many=True, required=False)
    active = serializers.BooleanField(required=False)

class ReceiptSerializerList(serializers.ModelSerializer):
    records = RecordSerializerList(many=True, read_only=True)
    class Meta:
        model = Receipt
        fields = '__all__'
        depth = 1

class ReceiptResponseSerializer(serializers.Serializer):
    statusCode = serializers.IntegerField()
    statusDesc = serializers.CharField()
    result = ReceiptSerializerList()

class ReceiptsResponseSerializer(serializers.Serializer):
    statusCode = serializers.IntegerField()
    statusDesc = serializers.CharField()
    result = ReceiptSerializerList(many=True)

class SystemUnitsSerializer(serializers.Serializer):
    unitName = serializers.CharField(max_length=100)
    unitCode = serializers.CharField(max_length=100)
    unitSymbol = serializers.CharField(max_length=100)
    unitDescription = serializers.CharField()
    unitType = serializers.CharField(max_length=100)

class SystemUnitsSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = SystemUnits
        fields = '__all__'
        depth = 1

class SystemUnitResponseSerializer(serializers.Serializer):
    statusCode = serializers.IntegerField()
    statusDesc = serializers.CharField()
    result = SystemUnitsSerializerGet()

class SystemUnitsResponseSerializer(serializers.Serializer):
    statusCode = serializers.IntegerField()
    statusDesc = serializers.CharField()
    result = SystemUnitsSerializerGet(many=True)

class FXSerializer(serializers.Serializer):
    sendCurrency = serializers.CharField(max_length=100)
    receiveCurrency = serializers.CharField(max_length=100)
    exchangeRate = serializers.FloatField()

class FXSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = FX
        fields = '__all__'
        depth = 1

class FXResponseSerializer(serializers.Serializer):
    statusCode = serializers.IntegerField()
    statusDesc = serializers.CharField()
    result = FXSerializerGet()

class FXsResponseSerializer(serializers.Serializer):
    statusCode = serializers.IntegerField()
    statusDesc = serializers.CharField()
    result = FXSerializerGet(many=True)

class CurrencySerializer(serializers.Serializer):
    currencyCode = serializers.CharField(max_length=100)
    currencyName = serializers.CharField(max_length=100, required=True)
    currencySymbol = serializers.CharField(max_length=100, required=True)

class CurrencySerializerList(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'
        depth = 1

class CurrencyResponseSerializer(serializers.Serializer):
    statusCode = serializers.IntegerField()
    statusDesc = serializers.CharField()
    result = CurrencySerializerList()

class CurrenciesResponseSerializer(serializers.Serializer):
    statusCode = serializers.IntegerField()
    statusDesc = serializers.CharField()
    result = CurrencySerializerList(many=True)