from django.contrib import admin
from .models import RecommendationModel, UserRecommendation, RecommendedBook, Report, ErrorLog, SystemConfig

admin.site.register(RecommendationModel)
admin.site.register(UserRecommendation)
admin.site.register(RecommendedBook)
admin.site.register(Report)
admin.site.register(ErrorLog)
admin.site.register(SystemConfig)
