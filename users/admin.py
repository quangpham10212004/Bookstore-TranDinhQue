from django.contrib import admin
from .models import Member, Customer, Admin, Address, UserSession, UserActivityLog, NotificationType, Notification, EmailVerification, PasswordResetToken

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')

admin.site.register(Customer)
admin.site.register(Admin)
admin.site.register(Address)
admin.site.register(UserSession)
admin.site.register(UserActivityLog)
admin.site.register(NotificationType)
admin.site.register(Notification)
admin.site.register(EmailVerification)
admin.site.register(PasswordResetToken)
