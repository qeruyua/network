from django.db import models

# Create your models here.
class Features(models.Model):
    id = models.AutoField(primary_key =  True)
    src = models.CharField(max_length=32)
    srcport = models.CharField(max_length=32)
    dst = models.CharField(max_length=32)
    dstport = models.CharField(max_length=32)
    timestamp = models.CharField(max_length=32)
    time = models.CharField(max_length=32)
    proto = models.CharField(max_length=10)

class FlowFeature(models.Model):
    flowid  = models.AutoField(primary_key =  True)
    flowsrc = models.CharField(max_length=32)
    flowsrcport = models.CharField(max_length=32)
    flowdst = models.CharField(max_length=32)
    flowdstport = models.CharField(max_length=32)
    flowproto = models.CharField(max_length=10)

class SessionFeatures(models.Model):
    sessionid = models.AutoField(primary_key =  True)
    sessionaddr1 = models.CharField(max_length=32)
    sessionport1 = models.CharField(max_length=32)
    sessionaddr2 = models.CharField(max_length=32)
    sessionport2 = models.CharField(max_length=32)
    sessionproto = models.CharField(max_length=10)