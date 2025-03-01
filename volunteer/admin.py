from django.contrib import admin
from .models import * 



class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_role', 'email', 'company', 'first_name', 'last_name', 'is_active')  # Поля в списке
    fields = ('id', 'company', 'email', 'first_name', 'last_name', 'password', 'is_manager', 'activation_code', 'is_active')  # Все поля отображаются
    readonly_fields = ('id',)  # ID нельзя изменять
    list_filter = ('is_manager', 'company')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Делаем email, first_name, last_name и password необязательными
        for field in ['email', 'first_name', 'last_name', 'password']:
            form.base_fields[field].required = False
            form.base_fields[field].blank = True
        return form
    
    def get_role(self, obj):
        return "Manager" if obj.is_manager else "Volunteer"

    get_role.short_description = "Role"  # Заголовок в админке


admin.site.register(Company)
admin.site.register(User, UserAdmin)

