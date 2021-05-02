from django.contrib import admin

# Register your models here.

#将models创建的表，添加到admin后台中

from  upfile import models
admin.site.register(models.Features)
admin.site.register(models.FlowFeature)
admin.site.register(models.SessionFeatures)
