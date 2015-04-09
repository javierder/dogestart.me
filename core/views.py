from django.core.mail import send_mail

from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from core.forms import BountyForm
from django.contrib.auth.decorators import login_required
from core.models import Bounty, BountyMessage, EarnedLog
from django.contrib import messages
import datetime
from scripts import dogecoinrpc

from account.signals import email_confirmed
from account.models import Account

from django.dispatch import receiver
from django.db.models import Sum

OUR_FEE = 0.01

# @receiver(email_confirmed)
# def email_confirmed_receiver(sender, **kwargs):
# 	email = sender.email_address
# 	acc = Account.objects.filter(user__email=email)
# 	assing_new_internal_address(acc)

# def assing_new_internal_address(acc):
# 	acc_add = AccountAddress.objects.filter(account=acc)
# 	if acc_add.exists():
# 		acc_add = acc_add[0]
# 	else:
# 		acc_add = AccountAddress()
# 		acc_add.account = acc

# 	try:
# 		dogerpc = _get_rpc()
# 		# raise E

# 		new_address = dogerpc.getnewaddress()
# 		acc_add.address = new_address
# 		acc_add.save()
# 	except:
# 		pass


# 	# print("Request finished!")


PAGE_SIZE = 10
def home(request):
        messages.add_message(request, messages.SUCCESS,"Welcome to DogeStart.Me; this site will allow you to create and redeem bounties based on Dogecoin!")
	
	return redirect("bounties_active")
	context = RequestContext(request)

	return render_to_response("homepage.html",context_instance=context)

@login_required
def approve_redeem(request, id):
	
	m = get_object_or_404(BountyMessage,pk=id)

	if m.bounty.author != request.user.account:
		return redirect("view_bounty", m.bounty.pk)

	# m.approved = True
	m.save()
	b = m.bounty
	b.completed = datetime.datetime.now()
	b.save()

	log = EarnedLog()
	log.account = m.author
	log.bounty = b
	log.message = m
	log.amount =  b.amount * (1 - OUR_FEE)
	log.save()
	
	messages.add_message(request, messages.SUCCESS,"Bounty Redeemed!")
	smessage = "You have won a bounty!: http://http://dogestart.me/bounties/view/%d/\n Thanks!\nDogeStart.me" % m.bounty.id
	send_mail('DogeStart.Me: You have won a bounty', smessage, 'doge@dogestart.me',
    		[m.author.user.email], fail_silently=True)
	return redirect("view_bounty", m.bounty.pk)

@login_required
def withdraw(request):
	context = RequestContext(request)
	earnlog = EarnedLog.objects.filter(withdrawn=False).filter(account=request.user.account).order_by("-pk")

	context["total"] = earnlog.aggregate(Sum('amount'))["amount__sum"]
	context["earnlog"] = earnlog

	if request.POST :
		address = request.POST.get("address","")
		if address != "":

			total = context["total"] -1 
			try:
				conn = _get_rpc()
				txid = conn.sendtoaddress(address, total, "from dogestartme")
			except:
				messages.add_message(request, messages.ERROR ,"Problem with the doge network")
			else:
				messages.add_message(request, messages.SUCCESS ,"withdrawn, transaction id: %s" % txid)
				for l in earnlog:
					l.withdrawn = True
					l.save()
			return redirect("withdraw")








	return render_to_response("withdraw.html",context_instance=context)

def view_bounty(request, id):
	context = RequestContext(request)

	bounty = get_object_or_404(Bounty,pk=id)
	context["bounty"] = bounty
	context["bmessages"] = BountyMessage.objects.filter(bounty=bounty).order_by("-created")
	
	return render_to_response("view_bounty.html",context_instance=context)

@login_required
def redeem_bounty(request, id):

	bounty = get_object_or_404(Bounty,pk=id)
	if request.POST.get("text","") == "":
		return redirect("view_bounty",id=id)
	msg = BountyMessage()
	msg.author = request.user.account
	msg.bounty = bounty
	msg.text = request.POST["text"]

	msg.save()

	messages.add_message(request, messages.SUCCESS,"Message sent!")
	smessage = "A new redeem attemp has been put in your bounty: http://dogestart.me/bounties/view/%d/\n Thanks!\nDogeStart.me" % bounty.id 
	send_mail('DogeStart.Me: New redeem attemp in your bounty', smessage, 'doge@dogestart.me',
    		[bounty.author.user.email], fail_silently=True)
	return redirect("view_bounty",id=id)




@login_required
def bounties_applied(request, page=1):
	
	context = RequestContext(request)
	page = int(request.GET.get("page",1))

	bounties = Bounty.objects.filter(funded=True).filter(completed=None).filter(bountymessage__author=request.user.account).order_by("-created")


	bounties = bounties[(page-1) * PAGE_SIZE:]
	bounties = bounties[:PAGE_SIZE]

	context["bounties"]  = bounties

	context["bounties"]  =bounties
	context["tab"] = "My Related Bounties"
	context["loadmoreurl"] = "bounties_applied"
	context["mytitle"] = "List of my related bounties"
	if request.GET.get("ajax","") == "1":
		return render_to_response("bounties_list.html",context_instance=context)

	else:
		return render_to_response("bounties.html",context_instance=context)

@login_required		
def bounties_mine(request):
	context = RequestContext(request)
	page = int(request.GET.get("page",1))


	bounties = Bounty.objects.filter(author=request.user.account).order_by("-created")

	bounties = bounties[(page-1) * PAGE_SIZE:]
	bounties = bounties[:PAGE_SIZE]

	context["bounties"]  = bounties
	context["mytitle"] = "List of my bounties"


	context["bounties"]  =bounties
	context["tab"] = "My Bounties"
	context["mine"] = True
	context["loadmoreurl"] = "bounties_mine"


	if request.GET.get("ajax","") == "1":
		return render_to_response("bounties_list.html",context_instance=context)

	else:
		return render_to_response("bounties.html",context_instance=context)

def bounties_active(request):

	page = int(request.GET.get("page",1))
	context = RequestContext(request)

	bounties = Bounty.objects.filter(funded=True).filter(completed=None).order_by("-created")

	bounties = bounties[(page-1) * PAGE_SIZE:]
	bounties = bounties[:PAGE_SIZE]

	context["mytitle"] = "List of active & funded bounties"


	context["bounties"]  = bounties
	context["loadmoreurl"] = "bounties_active"
	if request.GET.get("ajax","") == "1":
		return render_to_response("bounties_list.html",context_instance=context)

	else:
		return render_to_response("bounties.html",context_instance=context)



@login_required
def new_bounty(request):

	context = RequestContext(request)

	if request.POST:
		
		form = BountyForm(request.POST)
		if form.is_valid():
			try:
				dogerpc = _get_rpc()
				# raise E

				new_address = dogerpc.getnewaddress()
			except:
				messages.add_message(request, messages.ERROR,"Couldn't connect to Doge RPC. Try again please.")
			else:
				# print request.user.account
				bounty = form.save(commit=False)
				bounty.author = request.user.account
				bounty.save()

				new_address = dogerpc.getnewaddress()
				bounty.address = new_address
				bounty.save()
				smessage = "New bounty created!: http://dogestart.me/bounties/view/%d/\n Thanks!\nDogeStart.me" % bounty.id
				send_mail('DogeStart.Me: new bounty', smessage, '',
					    [""], fail_silently=True)

				messages.add_message(request, messages.SUCCESS,"New DogeBounty Created!")
				return redirect("view_bounty",id=bounty.pk)

	else:
		form = BountyForm()

	context["form"] = form
	return render_to_response("new_bounty.html",context_instance=context)



def _get_rpc():

	serverIP = '127.0.0.1'
	serverPort = '22555'#44555'
	user = 'dogecoinrpc'
	password = ''#'
	conn = dogecoinrpc.connect_to_remote(user, password, host=serverIP, port=serverPort)
	return conn

