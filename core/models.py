from django.db import models
from account.models import Account
# Create your models here.
from mailhide import ashtml



# class AccountAddress(models.Model):
# 	account = models.ForeignKey(Account)
# 	address = models.CharField(max_length=300)



class Tag(models.Model):
	name = models.CharField(max_length=200)

class Bounty(models.Model):
	author = models.ForeignKey(Account)
	title = models.CharField(max_length=300)
	description = models.TextField()
	tags = models.ManyToManyField(Tag)
	completed = models.DateTimeField(null=True,default=None)
	funded = models.BooleanField(default=False)
	address = models.CharField(default="",max_length=300)
	amount = models.FloatField()
	created = models.DateTimeField(auto_now_add=True)
	total_bounties = models.IntegerField(default=1,verbose_name="Number of Redeeems you'll accept")

	def get_crypted(self):
		return ashtml(self.author.user.email,"01IOI1PYgLnMhTNWjBPpJ6SQ==","8afa6dd86e803d00456853387c56ae00")


class BountyMessage(models.Model):
	author = models.ForeignKey(Account)
	text = models.TextField()
	bounty = models.ForeignKey(Bounty)
	created = models.DateTimeField(auto_now_add=True)
	approved = models.NullBooleanField(default=False, null=True)

class FullFillMent(models.Model):
	author = models.ForeignKey(Account)
	bounty = models.ForeignKey(Bounty)
	created = models.DateTimeField(auto_now_add=True)


class EarnedLog(models.Model):
	account = models.ForeignKey(Account)
	bounty = models.ForeignKey(Bounty)
	message = models.ForeignKey(BountyMessage)
	amount = models.FloatField(default=0)
	withdrawn = models.BooleanField(default=False)

