from django.contrib.auth.decorators import login_required


@login_required
def details(request, template_name="homepage/details.html"):
	from django.http import HttpResponseRedirect
	return HttpResponseRedirect('/time-spent/')