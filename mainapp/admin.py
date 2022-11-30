from django.contrib import admin
from .models import Profile, Transaction, BetEntry, BetWin, ResultSettings
# Register your models here.

admin.site.register(Profile)
admin.site.register(Transaction)
admin.site.register(BetEntry)
admin.site.register(BetWin)
admin.site.register(ResultSettings)