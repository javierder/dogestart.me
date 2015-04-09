from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin


urlpatterns = patterns("",
    url(r"^$", "core.views.home", name="home"),
    url(r"^bounties/active/$", "core.views.bounties_active", name="bounties_active"),
    url(r"^bounties/active/mine/$", "core.views.bounties_mine", name="bounties_mine"),
    url(r"^bounties/active/applied/$", "core.views.bounties_applied", name="bounties_applied"),

    url(r"^bounties/new_bounty/$", "core.views.new_bounty", name="new_bounty"),
    url(r"^bounties/view/(?P<id>\d+)/$", "core.views.view_bounty", name="view_bounty"),
    url(r"^bounties/redeem/(?P<id>\d+)/$", "core.views.redeem_bounty", name="redeem_bounty"),
    url(r"^bounties/approve/(?P<id>\d+)/$", "core.views.approve_redeem", name="approve_redeem"),
    url(r"^withdraw/$", "core.views.withdraw", name="withdraw"),

    


    url(r"^admin/", include(admin.site.urls)),
    url(r"^accounts/", include("account.urls")),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
