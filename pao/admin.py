from django.contrib import admin
from .models import Department, Expert, ContractNames, CheckEc, Post

# Register your models here.
admin.site.register(Department )
admin.site.register(Expert )
admin.site.register(ContractNames )
admin.site.register(CheckEc )
admin.site.register(Post )