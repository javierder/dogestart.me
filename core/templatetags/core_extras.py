from django import template
from core.models import EarnedLog
from django.db.models import Sum


register = template.Library()


def total_avaliable(account):
	data = EarnedLog.objects.filter(account=account).filter(withdrawn=False).aggregate(Sum('amount'))["amount__sum"]
	if data == None:
		data = 0
	return data
register.simple_tag(total_avaliable)
