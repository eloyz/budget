from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

def details(request, template_name="details.html"):

	return render_to_response(
		template_name, 
		{}, context_instance=RequestContext(request)
	)