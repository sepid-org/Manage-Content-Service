import csv

from django.contrib import admin
from django.http import HttpResponse

from apps.scoring.models import ScoreType, Cost, Reward, Transaction


@admin.register(Cost)
class CriteriaCustomAdmin(admin.ModelAdmin):

    def get_passed_receipts(self, request, queryset):
        file = open('passed-users.csv', 'w', encoding="utf-8")
        writer = csv.writer(file)
        writer.writerow(['username', 'name', 'last_name', 'phone_number'])
        if len(queryset) > 1:
            return
        criteria = queryset[0]
        registration_receipts = getattr(
            criteria, 'paper').state.fsm.program.registration_form.registration_receipts.all()

        for receipt in registration_receipts:
            if criteria.evaluate(receipt.user):
                writer.writerow(
                    [receipt.user.id, receipt.user.first_name, receipt.user.last_name, receipt.user.phone_number])

        file.close()

        f = open('passed-users.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=passed-users.csv'
        return response

    actions = [get_passed_receipts]


admin.site.register(ScoreType)
admin.site.register(Reward)
admin.site.register(Transaction)
