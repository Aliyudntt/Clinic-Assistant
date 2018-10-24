from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect


from allauth.account.views import PasswordChangeView

class RedirectDashBoardAfterPasswordChange(PasswordChangeView):
    @property
    def success_url(self):
        return "/authentication/dashboard/"

pass_change_view = login_required(RedirectDashBoardAfterPasswordChange.as_view())

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login/")


@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard_home.html',{})