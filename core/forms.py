from django.forms import ModelForm
from core.models import Bounty


class BountyForm(ModelForm):
    class Meta:
        model = Bounty
        fields = ['title', 'description', 'amount', 'total_bounties']

