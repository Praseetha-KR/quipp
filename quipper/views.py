from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from quipper.models import Choice, Poll

class IndexView(generic.ListView):
	template_name = 'quipper/index.html'
	context_object_name = 'latest_poll_list'

	def get_queryset(self):
		return Poll.objects.order_by('-pub_date')[:5]		
	# latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
	# context = {'latest_poll_list': latest_poll_list}
	# return render(request, 'quipper/index.html', context)

class DetailView(generic.DetailView):
	model = Poll
	template_name = 'quipper/detail.html'
	# poll = get_object_or_404(Poll, pk=poll_id)
	# return render(request, 'quipper/detail.html', {'poll': poll})

class ResultsView(generic.DetailView):
	model = Poll
	template_name = 'quipper/results.html'
    # poll = get_object_or_404(Poll, pk=poll_id)
    # return render(request, 'quipper/results.html', {'poll': poll})

def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'quipper/detail.html', {
			'poll': p,
			'error_message': "You didn't select a choice."
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
    	return HttpResponseRedirect(reverse('quipper:results', args=(p.id,)))