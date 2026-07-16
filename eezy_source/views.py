from django.utils import timezone
from rest_framework import generics
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

import logging

from eezy_source.models import Currency, ProcessConfig, SystemUnits, FX, Receipt, Record, Business
logger = logging.getLogger("django")

from eezy_source.serializers import ConfigurationSerializer, ConfigurationSerializerGet, ConfigurationsResponseSerializer, ConfigurationResponseSerializer, CurrenciesResponseSerializer, CurrencyResponseSerializer, CurrencySerializer, CurrencySerializerList, LoginResponseSerializer, LoginSerializer, ReceiptSerializer, RecordSerializer, ReceiptSerializerList, ReceiptResponseSerializer, ReceiptsResponseSerializer, SystemUnitsSerializer, SystemUnitsSerializerGet, RegisterResponseSerializer, SystemUnitsResponseSerializer, FXSerializer, FXSerializerGet, FXResponseSerializer, FXsResponseSerializer, UserSerializer 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

class Resp:
	def __init__(self, statusDesc, result, statusCode):
		self.statusDesc=statusDesc
		self.result=result
		self.statusCode=statusCode

# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        message = "User registered successfully"
        status_ = status.HTTP_201_CREATED
        resp = Resp(statusDesc=message, statusCode=status_, result=token.key)
        return Response(RegisterResponseSerializer(resp).data, status=status_)


class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        message = "User retrieved successfully"
        status_ = status.HTTP_200_OK
        serializer = UserSerializer(request.user)
        resp = Resp(statusDesc=message, statusCode=status_, result=serializer.data)
        return Response(resp.__dict__, status=status_)

        

class UserLoginView(APIView):
   def post(self, request):
        logger.info("Login attempt received")
        message = "Login failed"
        status_ = status.HTTP_400_BAD_REQUEST
        result = None

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['phoneNumber']
            password = serializer.validated_data['password']
            logger.info("Login validation passed for phoneNumber=%s", username)
            user = authenticate(username=username, password=password)  # Authenticate the user
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)  # Create or retrieve a token for the user
                message = "Login successful"
                status_ = status.HTTP_200_OK
                result = token.key
                logger.info("Login successful for phoneNumber=%s", username)
            else:
                message = "Invalid phone number or password"
                logger.warning("Login authentication failed for phoneNumber=%s", username)
        else:
            message = "Invalid login payload"
            logger.warning("Login payload validation failed: %s", serializer.errors)
        resp = Resp(statusDesc=message, statusCode=status_, result=result)
        return Response(LoginResponseSerializer(resp).data, status=status_)

class ConfigurationViewSet(viewsets.ViewSet):
    lookup_field = 'processCode'
    lookup_url_kwarg = 'pk'
    lookup_value_regex = '[^/]+'

    def list(self, request):
        # Logic to list configurations
        message = "Configurations retrieved successfully"
        status_ = status.HTTP_200_OK
        try:
            configurations = ProcessConfig.objects.filter(active=True)
            logger.info("Retrieved configurations: %s", configurations)
            serializer = ConfigurationSerializerGet(configurations, many=True).data
            logger.info("Serialized configurations: %s", serializer)
            resp = Resp(statusDesc=message, statusCode=status_, result=serializer)
            return Response(ConfigurationsResponseSerializer(resp).data, status=status_)
        except Exception as e:
            logger.error("Error retrieving configurations: %s", str(e))
            message = "Error retrieving configurations"
            status_ = status.HTTP_500_INTERNAL_SERVER_ERROR
            resp = Resp(statusDesc=message, statusCode=status_, result=None)
            return Response(ConfigurationsResponseSerializer(resp).data, status=status_)

    def create(self, request):
        # Logic to create a new language
        message = "Configuration created successfully"
        status_ = status.HTTP_201_CREATED
        serializer = ConfigurationSerializer(data=request.data)
        if serializer.is_valid():
            business_name = serializer.validated_data.get('businessName')
            business_phone = serializer.validated_data.get('businessPhone')
            business_email = serializer.validated_data.get('businessEmail')
            business_address = serializer.validated_data.get('businessAddress')

            business = Business.objects.create(
                businessName=business_name,
                businessPhone=business_phone,
                businessEmail=business_email,
                businessAddress=business_address
            )

            business.save()
            
            process_code = serializer.validated_data.get('processCode')
            seller_shipper_delivery_fee = serializer.validated_data.get('sellerShipperDeliveryFee')
            seller_shipper_delivery_fee_unit = serializer.validated_data.get('sellerShipperDeliveryFeeUnit')
            handlingFee = serializer.validated_data.get('handlingFee')
            handlingFeeUnit = serializer.validated_data.get('handlingFeeUnit')
            weightUnit = serializer.validated_data.get('weightUnit')
            shippingMode = serializer.validated_data.get('shippingMode')
            customRate = serializer.validated_data.get('customRate')
            customRateUnit = serializer.validated_data.get('customRateUnit')
            shippingMargin = serializer.validated_data.get('shippingMargin')
            shippingMarginUnit = serializer.validated_data.get('shippingMarginUnit')
            defaultCurrency = serializer.validated_data.get('defaultCurrency')
            try:
                configuration = ProcessConfig.objects.create(
                    processCode=process_code,
                    sellerShipperDeliveryFee=seller_shipper_delivery_fee,
                    sellerShipperDeliveryFeeUnit=seller_shipper_delivery_fee_unit,
                    handlingFee=handlingFee,
                    handlingFeeUnit=handlingFeeUnit,
                    weightUnit=weightUnit,
                    shippingMode=shippingMode,
                    customRate=customRate,
                    customRateUnit=customRateUnit,
                    shippingMargin=shippingMargin,
                    shippingMarginUnit=shippingMarginUnit,
                    defaultCurrency=defaultCurrency,
                    business=business
                )
                configuration.save()
                
                message = "Configuration created successfully"
                status_ = status.HTTP_201_CREATED
                resp = Resp(statusDesc=message, statusCode=status_, result=ConfigurationSerializerGet(configuration).data)
                return Response(ConfigurationResponseSerializer(resp).data, status=status_)
            except Exception as e:
                logger.error("Error creating configuration: %s", str(e))
                message = "Configuration creation failed"
                status_ = status.HTTP_400_BAD_REQUEST
                resp = Resp(statusDesc=message, statusCode=status_, result=str(e))
                return Response(ConfigurationResponseSerializer(resp).data, status=status_)
        else:
            logger.error("Configuration creation failed: %s", serializer.errors)
            message = "Configuration creation failed"
            status_ = status.HTTP_400_BAD_REQUEST
            resp = Resp(statusDesc=message, statusCode=status_, result=serializer.errors)
            return Response(ConfigurationResponseSerializer(resp).data, status=status_)
    
    def update(self, request, pk=None):
        logger.info("Received request data for configuration update: %s", request.data)
        message = "Configuration created successfully"
        status_ = status.HTTP_201_CREATED
        serializer = ConfigurationSerializer(data=request.data)
        if serializer.is_valid():
            process_code = serializer.validated_data.get('processCode')
            seller_shipper_delivery_fee = serializer.validated_data.get('sellerShipperDeliveryFee')
            seller_shipper_delivery_fee_unit = serializer.validated_data.get('sellerShipperDeliveryFeeUnit')
            handlingFee = serializer.validated_data.get('handlingFee')
            handlingFeeUnit = serializer.validated_data.get('handlingFeeUnit')
            weightUnit = serializer.validated_data.get('weightUnit')
            shippingMode = serializer.validated_data.get('shippingMode')
            customRate = serializer.validated_data.get('customRate')
            customRateUnit = serializer.validated_data.get('customRateUnit')
            shippingMargin = serializer.validated_data.get('shippingMargin')
            shippingMarginUnit = serializer.validated_data.get('shippingMarginUnit')
            defaultCurrency = serializer.validated_data.get('defaultCurrency')
            try:
                process_code_lookup = pk or process_code
                configuration = ProcessConfig.objects.filter(processCode=process_code_lookup).first()
                if configuration:
                    configuration.sellerShipperDeliveryFee = seller_shipper_delivery_fee
                    configuration.sellerShipperDeliveryFeeUnit = seller_shipper_delivery_fee_unit
                    configuration.handlingFee = handlingFee
                    configuration.handlingFeeUnit = handlingFeeUnit
                    configuration.weightUnit = weightUnit
                    configuration.shippingMode = shippingMode
                    configuration.customRate = customRate
                    configuration.customRateUnit = customRateUnit
                    configuration.shippingMargin = shippingMargin
                    configuration.shippingMarginUnit = shippingMarginUnit
                    configuration.defaultCurrency = defaultCurrency
                    configuration.save()

                    business_name = serializer.validated_data.get('businessName')
                    business_phone = serializer.validated_data.get('businessPhone')
                    business_email = serializer.validated_data.get('businessEmail')
                    business_address = serializer.validated_data.get('businessAddress')

                    business = Business.objects.filter(businessId=configuration.business.businessId).first()

                    if business:
                        business.businessName = business_name
                        business.businessPhone = business_phone
                        business.businessEmail = business_email
                        business.businessAddress = business_address
                        business.save()

                    message = "Configuration created successfully"
                    status_ = status.HTTP_201_CREATED
                    resp = Resp(statusDesc=message, statusCode=status_, result=ConfigurationSerializerGet(configuration).data)
                    return Response(ConfigurationResponseSerializer(resp).data, status=status_)
                else:
                    business_name = serializer.validated_data.get('businessName')
                    business_phone = serializer.validated_data.get('businessPhone')
                    business_email = serializer.validated_data.get('businessEmail')
                    business_address = serializer.validated_data.get('businessAddress')

                    business = Business.objects.create(
                        businessName=business_name,
                        businessPhone=business_phone,
                        businessEmail=business_email,
                        businessAddress=business_address
                    )

                    business.save()
                    
                    process_code = serializer.validated_data.get('processCode')
                    seller_shipper_delivery_fee = serializer.validated_data.get('sellerShipperDeliveryFee')
                    seller_shipper_delivery_fee_unit = serializer.validated_data.get('sellerShipperDeliveryFeeUnit')
                    handlingFee = serializer.validated_data.get('handlingFee')
                    handlingFeeUnit = serializer.validated_data.get('handlingFeeUnit')
                    weightUnit = serializer.validated_data.get('weightUnit')
                    shippingMode = serializer.validated_data.get('shippingMode')
                    customRate = serializer.validated_data.get('customRate')
                    customRateUnit = serializer.validated_data.get('customRateUnit')
                    shippingMargin = serializer.validated_data.get('shippingMargin')
                    shippingMarginUnit = serializer.validated_data.get('shippingMarginUnit')
                    defaultCurrency = serializer.validated_data.get('defaultCurrency')
                    try:
                        configuration = ProcessConfig.objects.create(
                            processCode=process_code,
                            sellerShipperDeliveryFee=seller_shipper_delivery_fee,
                            sellerShipperDeliveryFeeUnit=seller_shipper_delivery_fee_unit,
                            handlingFee=handlingFee,
                            handlingFeeUnit=handlingFeeUnit,
                            weightUnit=weightUnit,
                            shippingMode=shippingMode,
                            customRate=customRate,
                            customRateUnit=customRateUnit,
                            shippingMargin=shippingMargin,
                            shippingMarginUnit=shippingMarginUnit,
                            defaultCurrency=defaultCurrency,
                            business=business
                        )
                        configuration.save()

                        message = "Configuration created successfully"
                        status_ = status.HTTP_201_CREATED
                        resp = Resp(statusDesc=message, statusCode=status_, result=ConfigurationSerializerGet(configuration).data)
                        return Response(ConfigurationResponseSerializer(resp).data, status=status_)
                    except Exception as e:
                        logger.error("Error creating configuration: %s", str(e))
                        message = "Configuration creation failed"
                        status_ = status.HTTP_400_BAD_REQUEST
                        resp = Resp(statusDesc=message, statusCode=status_, result=str(e))
                        return Response(ConfigurationResponseSerializer(resp).data, status=status_)
            except Exception as e:
                logger.error("Error creating configuration: %s", str(e))
                message = "Configuration creation failed"
                status_ = status.HTTP_400_BAD_REQUEST
                resp = Resp(statusDesc=message, statusCode=status_, result=str(e))
                return Response(ConfigurationResponseSerializer(resp).data, status=status_)
        else:
            logger.error("Configuration creation failed: %s", serializer.errors)
            message = "Configuration creation failed"
            status_ = status.HTTP_400_BAD_REQUEST
            resp = Resp(statusDesc=message, statusCode=status_, result=serializer.errors)
            return Response(ConfigurationResponseSerializer(resp).data, status=status_)
    
    def retrieve(self, request, pk=None):
        try:
            message = "Configuration retrieved successfully"
            status_ = status.HTTP_200_OK
            if not pk:
                status_ = status.HTTP_400_BAD_REQUEST
                message = "Invalid request"
                resp = Resp(statusDesc=message, statusCode=status_, result=None)
                return Response(ConfigurationResponseSerializer(resp).data, status=status_)

            configuration = ProcessConfig.objects.get(processCode=pk)
            serializer = ConfigurationSerializerGet(configuration)
            resp = Resp(statusDesc=message, statusCode=status_, result=serializer.data)
            return Response(ConfigurationResponseSerializer(resp).data, status=status_)
        except ProcessConfig.DoesNotExist:
            message = "Configuration not found"
            status_ = status.HTTP_404_NOT_FOUND
            resp = Resp(statusDesc=message, statusCode=status_, result=None)
            return Response(ConfigurationResponseSerializer(resp).data, status=status_)
        
    def destroy(self, request, pk=None):
        try:
            configuration = ProcessConfig.objects.get(pk=pk)
            configuration.delete()
            return Response({"message": "Configuration deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ProcessConfig.DoesNotExist:
            return Response({"error": "Configuration not found"}, status=status.HTTP_404_NOT_FOUND)
        
class SystemUnitsViewSet(viewsets.ViewSet):
    def list(self, request):
        # Logic to list system units
        message = "System units retrieved successfully"
        status_ = status.HTTP_200_OK
        try:
            system_units = SystemUnits.objects.all()
            logger.info("Retrieved system units: %s", system_units)
            serializer = SystemUnitsSerializerGet(system_units, many=True).data
            logger.info("Serialized system units: %s", serializer)
            resp = Resp(statusDesc=message, statusCode=status_, result=serializer)
            return Response(SystemUnitsResponseSerializer(resp).data, status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error retrieving system units: %s", str(e))
            message = "Error retrieving system units"
            status_ = status.HTTP_500_INTERNAL_SERVER_ERROR
            resp = Resp(statusDesc=message, statusCode=status_, result=None)
            return Response(SystemUnitsResponseSerializer(resp).data, status=status_)

    def create(self, request):
        # Logic to create a new system unit
        message = "System unit created successfully"
        status_ = status.HTTP_201_CREATED
        serializer = SystemUnitsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                name = serializer.validated_data.get('unitName')
                code = serializer.validated_data.get('unitCode')
                symbol = serializer.validated_data.get('unitSymbol')
                description = serializer.validated_data.get('unitDescription')
                unit_type = serializer.validated_data.get('unitType')
                system_unit = SystemUnits.objects.create(
                    unitName=name,
                    unitCode=code,
                    unitSymbol=symbol,
                    unitDescription=description,
                    unitType=unit_type
                )
                system_unit.save()
                message = "System unit created successfully"
                status_ = status.HTTP_201_CREATED
                resp = Resp(statusDesc=message, statusCode=status_, result=SystemUnitsSerializerGet(system_unit).data)
                return Response(SystemUnitsResponseSerializer(resp).data, status=status_)
            except Exception as e:
                logger.error("Error creating system unit: %s", str(e))
                message = "System unit creation failed"
                status_ = status.HTTP_400_BAD_REQUEST
                resp = Resp(statusDesc=message, statusCode=status_, result=str(e))
                return Response(SystemUnitsResponseSerializer(resp).data, status=status_)
        else:
            logger.error("System unit creation failed: %s", serializer.errors)
            message = "System unit creation failed"
            status_ = status.HTTP_400_BAD_REQUEST
            resp = Resp(statusDesc=message, statusCode=status_, result=serializer.errors)
            return Response(SystemUnitsResponseSerializer(resp).data, status=status_)
    
    def retrieve(self, request, pk=None):
        try:
            message = "System unit retrieved successfully"
            status_ = status.HTTP_200_OK
            system_unit = SystemUnits.objects.get(pk=pk)
            serializer = SystemUnitsSerializerGet(system_unit)
            resp = Resp(statusDesc=message, statusCode=status_, result=serializer.data)
            return Response(SystemUnitsResponseSerializer(resp).data, status=status_)
        except SystemUnits.DoesNotExist:
            message = "System unit not found"
            status_ = status.HTTP_404_NOT_FOUND
            resp = Resp(statusDesc=message, statusCode=status_, result=None)
            return Response(SystemUnitsResponseSerializer(resp).data, status=status_)
        
    def destroy(self, request, pk=None):
        try:
            system_unit = SystemUnits.objects.get(pk=pk)
            system_unit.delete()
            message = "System unit deleted successfully"
            status_ = status.HTTP_204_NO_CONTENT
            resp = Resp(statusDesc=message, statusCode=status_, result=None)
            return Response(SystemUnitsResponseSerializer(resp).data, status=status_)
        except SystemUnits.DoesNotExist:
            message = "System unit not found"
            status_ = status.HTTP_404_NOT_FOUND
            resp = Resp(statusDesc=message, statusCode=status_, result=None)
            return Response(SystemUnitsResponseSerializer(resp).data, status=status_)

class CurrencyViewSet(viewsets.ViewSet):
    def list(self, request):
        # Logic to list currencies
        message = "Currencies retrieved successfully"
        status_ = status.HTTP_200_OK
        try:
            currencies = Currency.objects.filter(active=True)
            logger.info("Retrieved currencies: %s", currencies)
            serializer = CurrencySerializerList(currencies, many=True).data
            logger.info("Serialized currencies: %s", serializer)
            resp = Resp(statusDesc=message, statusCode=status_, result=serializer)
            return Response(CurrenciesResponseSerializer(resp).data, status=status_)
        except Exception as e:
            logger.error("Error retrieving currencies: %s", str(e))
            message = "Error retrieving currencies"
            status_ = status.HTTP_500_INTERNAL_SERVER_ERROR
            resp = Resp(statusDesc=message, statusCode=status_, result=str(e))
            return Response(CurrenciesResponseSerializer(resp).data, status=status_)

    def create(self, request):
        # Logic to create a new currency
        logger.info("Received request data for currency creation: %s", request.data)
        message = "Currency created successfully"
        status_ = status.HTTP_201_CREATED
        serializer = CurrencySerializer(data=request.data)
        if serializer.is_valid():
            try:
                name = serializer.validated_data.get('currencyName')
                code = serializer.validated_data.get('currencyCode')
                symbol = serializer.validated_data.get('currencySymbol')
                currency = Currency.objects.create(
                    currencyName=name,
                    currencyCode=code,
                    currencySymbol=symbol,
                    active=True
                )
                currency.save()
                message = "Currency created successfully"
                status_ = status.HTTP_201_CREATED
                resp = Resp(statusDesc=message, statusCode=status_, result=CurrencySerializerList(currency).data)
                logger.info("Currency created successfully: %s", resp)
                return Response(CurrencyResponseSerializer(resp).data, status=status_)
            except Exception as e:
                logger.error("Error creating currency: %s", str(e))
                # return Response({"error": "Error creating currency"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                message = "Currency creation failed"
                status_ = status.HTTP_400_BAD_REQUEST
                resp = Resp(statusDesc=message, statusCode=status_, result=str(e))
                return Response(CurrencyResponseSerializer(resp).data, status=status_)
        else:
            logger.error("Currency creation failed: %s", serializer.errors)
            message = "Currency creation failed"
            status_ = status.HTTP_400_BAD_REQUEST
            resp = Resp(statusDesc=message, statusCode=status_, result=serializer.errors)
            return Response(CurrencyResponseSerializer(resp).data, status=status_)
    
    def retrieve(self, request, pk=None):
        logger.info("Retrieving currency with ID: %s", pk)
        try:
            message = "Currency retrieved successfully"
            status_ = status.HTTP_200_OK
            currency = Currency.objects.get(pk=pk)
            serializer = CurrencySerializerList(currency)
            logger.info("Currency retrieved successfully: %s", serializer.data)
            resp = Resp(statusDesc=message, statusCode=status_, result=serializer.data)
            return Response(CurrencyResponseSerializer(resp).data, status=status_)
        except Currency.DoesNotExist:
            logger.error("Currency with ID %s not found", pk)
            message = "Currency not found"
            status_ = status.HTTP_404_NOT_FOUND
            resp = Resp(statusDesc=message, statusCode=status_, result=None)
            return Response(CurrencyResponseSerializer(resp).data, status=status_)
        
    def destroy(self, request, pk=None):
        try:
            currency = Currency.objects.get(pk=pk)
            currency.delete()
            message = "Currency deleted successfully"
            status_ = status.HTTP_204_NO_CONTENT
            resp = Resp(statusDesc=message, statusCode=status_, result=None)
            return Response(CurrencyResponseSerializer(resp).data, status=status_)
        except Currency.DoesNotExist:
            message = "Currency not found"
            status_ = status.HTTP_404_NOT_FOUND
            resp = Resp(statusDesc=message, statusCode=status_, result=None)
            logger.error("Currency with ID %s not found", pk)
            return Response(CurrencyResponseSerializer(resp).data, status=status_)
              
class FXViewSet(viewsets.ViewSet):
    def list(self, request):
        # Logic to list configurations
        message = "FX retrieved successfully"
        status_ = status.HTTP_200_OK
        try:
            configurations = FX.objects.filter(active=True)
            logger.info("Retrieved configurations: %s", configurations)
            serializer = FXSerializerGet(configurations, many=True).data
            logger.info("Serialized configurations: %s", serializer)
            resp = Resp(statusDesc=message, statusCode=status_, result=serializer)
            return Response(FXResponseSerializer(resp).data, status=status_)
        except Exception as e:
            logger.error("Error retrieving FX rates: %s", str(e))
            message = "Error retrieving FX rates"
            status_ = status.HTTP_500_INTERNAL_SERVER_ERROR
            resp = Resp(statusDesc=message, statusCode=status_, result=str(e))
            return Response(FXResponseSerializer(resp).data, status=status_)

    def create(self, request):
        # Logic to create a new FX rate
        message = "FX rate created successfully"
        status_ = status.HTTP_201_CREATED
        serializer = FXSerializer(data=request.data)
        if serializer.is_valid():
            sendCurrency = serializer.validated_data.get('sendCurrency')
            receiveCurrency = serializer.validated_data.get('receiveCurrency')
            exchangeRate = serializer.validated_data.get('exchangeRate')
            fx_rate = FX.objects.create(
                sendCurrency=sendCurrency,
                receiveCurrency=receiveCurrency,
                exchangeRate=exchangeRate,
                active=True
            )
            fx_rate.save()
            resp = Resp(statusDesc=message, statusCode=status_, result=FXSerializerGet(fx_rate).data)
            return Response(FXResponseSerializer(resp).data, status=status_)
        else:
            logger.error("FX rate creation failed: %s", serializer.errors)
            message = "FX rate creation failed"
            status_ = status.HTTP_400_BAD_REQUEST
            resp = Resp(statusDesc=message, statusCode=status_, result=serializer.errors)
            return Response(FXResponseSerializer(resp).data, status=status_)
    
    def retrieve(self, request, pk=None):
        try:
            message = "FX rate retrieved successfully"
            status_ = status.HTTP_200_OK
            fx_rate = FX.objects.get(pk=pk)
            serializer = FXSerializerGet(fx_rate)
            resp = Resp(statusDesc=message, statusCode=status_, result=serializer.data)
            return Response(FXResponseSerializer(resp).data, status=status_)
        except FX.DoesNotExist:
            message = "FX rate not found"
            status_ = status.HTTP_404_NOT_FOUND
            resp = Resp(statusDesc=message, statusCode=status_, result=None)
            return Response(FXResponseSerializer(resp).data, status=status_)
        
    def destroy(self, request, pk=None):
        try:
            fx_rate = FX.objects.get(pk=pk)
            fx_rate.active = False  # Mark the FX rate as inactive instead of deleting it
            fx_rate.save()
            message = "FX rate deleted successfully"
            status_ = status.HTTP_204_NO_CONTENT
            resp = Resp(statusDesc=message, statusCode=status_, result=None)
            return Response(FXResponseSerializer(resp).data, status=status_)
        except FX.DoesNotExist:
            message = "FX rate not found"
            status_ = status.HTTP_404_NOT_FOUND
            resp = Resp(statusDesc=message, statusCode=status_, result=None)
            return Response(FXResponseSerializer(resp).data, status=status_)
        
class ReceiptViewSet(viewsets.ViewSet):
    def list(self, request):
        # Logic to list receipts
        message = "Receipts retrieved successfully"
        status_ = status.HTTP_200_OK
        try:
            receipts = Receipt.objects.filter(active=True)
            logger.info("Retrieved receipts: %s", receipts)
            serializer = ReceiptSerializerList(receipts, many=True).data
            logger.info("Serialized receipts: %s", serializer)
            resp = Resp(statusDesc=message, statusCode=status_, result=serializer)
            return Response(ReceiptsResponseSerializer(resp).data, status=status_)
        except Exception as e:
            logger.error("Error retrieving receipts: %s", str(e))
            message = "Error retrieving receipts"
            status_ = status.HTTP_500_INTERNAL_SERVER_ERROR
            resp = Resp(statusDesc=message, statusCode=status_, result=str(e))
            return Response(ReceiptsResponseSerializer(resp).data, status=status_)

    def create(self, request):
        # Logic to create a new receipt
        logger.info("Received request data for receipt creation: %s", request.data)
        message = "Receipt created successfully"
        status_ = status.HTTP_201_CREATED
        serializer = ReceiptSerializer(data=request.data)
        if serializer.is_valid():
            try:
                receiptName = serializer.validated_data.get('receiptName')
                receiptCode = serializer.validated_data.get('receiptCode')
                createdBy = serializer.validated_data.get('createdBy')
                receipt = Receipt.objects.create(
                    receiptName=receiptName,
                    receiptCode=receiptCode,
                    active=True,
                    created_by=createdBy if createdBy else (request.user.username if request.user.is_authenticated else 'Anonymous'),
                    updated_by=createdBy if createdBy else (request.user.username if request.user.is_authenticated else 'Anonymous')
                )
                receipt.save()

                try:
                    records_data = request.data.get('records', [])
                    for record_data in records_data:
                        itemName = record_data.get('itemName')
                        itemCost = record_data.get('itemCost')
                        quantity = record_data.get('quantity')
                        weight = record_data.get('weight')
                        deliveryFee = record_data.get('deliveryFee')
                        totalCost = itemCost * quantity if itemCost and quantity else None
                        Record.objects.create(
                            itemName=itemName,
                            itemCost=itemCost,
                            quantity=quantity,
                            weight=weight,
                            deliveryFee=deliveryFee,
                            totalCost=totalCost,
                            receipt=receipt,
                            active=True
                        ).save()
                    
                    message = "Receipt created successfully"
                    status_ = status.HTTP_201_CREATED
                    resp = Resp(statusDesc=message, statusCode=status_, result=ReceiptSerializerList(receipt).data)
                    return Response(ReceiptResponseSerializer(resp).data, status=status_)
                except Exception as e:
                    logger.error("Error creating records for receipt: %s", str(e))
                    message = "Receipt creation failed"
                    status_ = status.HTTP_400_BAD_REQUEST
                    resp = Resp(statusDesc=message, statusCode=status_, result=str(e))
                    return Response(ReceiptResponseSerializer(resp).data, status=status_)
            except Exception as e:
                logger.error("Error creating receipt: %s", str(e))
                message = "Receipt creation failed"
                status_ = status.HTTP_400_BAD_REQUEST
                resp = Resp(statusDesc=message, statusCode=status_, result=str(e))
                return Response(ReceiptResponseSerializer(resp).data, status=status_)
        else:
            logger.error("Receipt creation failed: %s", serializer.errors)
            message = "Receipt creation failed"
            status_ = status.HTTP_400_BAD_REQUEST
            resp = Resp(statusDesc=message, statusCode=status_, result=serializer.errors)
            return Response(ReceiptResponseSerializer(resp).data, status=status_)
    
    def retrieve(self, request, pk=None):
        try:
            message = "Receipt retrieved successfully"
            status_ = status.HTTP_200_OK
            receipt = Receipt.objects.get(pk=pk)
            serializer = ReceiptSerializerList(receipt)
            resp = Resp(statusDesc=message, statusCode=status_, result=serializer.data)
            return Response(ReceiptResponseSerializer(resp).data, status=status_)
        except Receipt.DoesNotExist:
            message = "Receipt not found"
            status_ = status.HTTP_404_NOT_FOUND
            resp = Resp(statusDesc=message, statusCode=status_, result=None)
            return Response(ReceiptResponseSerializer(resp).data, status=status_)
        
    def destroy(self, request, pk=None):
        try:
            receipt = Receipt.objects.get(pk=pk)
            receipt.delete()
            message = "Receipt deleted successfully"
            status_ = status.HTTP_204_NO_CONTENT
            resp = Resp(statusDesc=message, statusCode=status_, result=None)
            return Response(ReceiptResponseSerializer(resp).data, status=status_)
        except Receipt.DoesNotExist:
            message = "Receipt not found"
            status_ = status.HTTP_404_NOT_FOUND
            resp = Resp(statusDesc=message, statusCode=status_, result=None)
            return Response(ReceiptResponseSerializer(resp).data, status=status_)