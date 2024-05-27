from django.contrib import admin
from polls.models import Poll, Type, Question, Possibility

# Register your models here.

admin.site.register(Poll)
admin.site.register(Type)
admin.site.register(Question)
admin.site.register(Possibility)