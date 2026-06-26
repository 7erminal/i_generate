from django.db import models

# Create your models here.
class Business(models.Model):
    businessId = models.AutoField(primary_key=True)
    businessName = models.CharField(max_length=100, null=True, blank=True)
    businessPhone = models.CharField(max_length=100, null=True, blank=True)
    businessEmail = models.CharField(max_length=100, null=True, blank=True)
    businessAddress = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

class ProcessConfig(models.Model):
    processConfigId = models.AutoField(primary_key=True)
    processCode = models.CharField(max_length=100)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='process_business')
    sellerShipperDeliveryFee = models.FloatField(null=True, blank=True)
    sellerShipperDeliveryFeeUnit = models.CharField(max_length=100, null=True, blank=True)
    handlingFee = models.FloatField(null=True, blank=True)
    handlingFeeUnit = models.CharField(max_length=100, null=True, blank=True)
    weightUnit = models.CharField(max_length=100, null=True, blank=True)
    shippingMode = models.CharField(max_length=100, null=True, blank=True)
    customRate = models.FloatField(null=True, blank=True)
    customRateUnit = models.CharField(max_length=100, null=True, blank=True)
    shippingMargin = models.FloatField(null=True, blank=True)
    shippingMarginUnit = models.CharField(max_length=100, null=True, blank=True)
    defaultCurrency = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

class Receipt(models.Model):
    receiptId = models.AutoField(primary_key=True)
    receiptCode = models.CharField(max_length=100)
    receiptName = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

class Record(models.Model):
    recordId = models.AutoField(primary_key=True)
    itemName = models.CharField(max_length=40)
    itemCost = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    totalCost = models.FloatField(null=True, blank=True)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='record_receipt')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    active = models.SmallIntegerField(null=True, blank=True)

class SystemUnits(models.Model):
    systemUnitId = models.AutoField(primary_key=True)
    unitName = models.CharField(max_length=100, null=True, blank=True)
    unitCode = models.CharField(max_length=100, null=True, blank=True)
    unitSymbol = models.CharField(max_length=100, null=True, blank=True)
    unitDescription = models.TextField(null=True, blank=True)
    unitType = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

class Currency(models.Model):
    currencyId = models.AutoField(primary_key=True)
    currencyName = models.CharField(max_length=100, null=True, blank=True)
    currencyCode = models.CharField(max_length=100, null=True, blank=True)
    currencySymbol = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

class FX(models.Model):
    fxId = models.AutoField(primary_key=True)
    sendCurrency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='fx_from_currency')
    receiveCurrency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='fx_to_currency')
    exchangeRate = models.FloatField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)