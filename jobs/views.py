from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView, ListView,
    DetailView, RedirectView,
)

from jobs.models import Job, JobProposal
from users.models import User


class JobListView(ListView):
    """
    Show a list of jobs.
    """
    model = Job
    ordering = ('job_title',)
    context_object_name = 'jobs'
    template_name = 'jobs/job_list.html'
    queryset = Job.objects.all()


@method_decorator([login_required], name='dispatch')
class JobCreateView(CreateView):
    """
    Create a job.
    """
    model = Job
    fields = ('job_title', 'job_description', 'price', 'tags', 'document')
    template_name = 'jobs/job_add_form.html'

    def form_valid(self, form):
        job = form.save(commit=False)
        job.owner = self.request.user

        job.save()
        form.save_m2m()
        messages.success(self.request, 'The job was created with success!')
        return redirect('jobs:job_detail', job.pk)


@method_decorator([login_required], name='dispatch')
class JobDetailView(DetailView):
    """
    Show the job's detail.
    """
    model = Job
    template_name = 'jobs/job_detail.html'

    def get_context_data(self, **kwargs):
        job_id = self.kwargs.get('pk')
        job = Job.objects.get(pk=job_id)
        if job.owner != self.request.user and self.request.user in job.freelancers:
            kwargs['current_proposal'] = JobProposal.objects.get(
                job__pk=job_id,
                freelancer=self.request.user)

        context = super().get_context_data(**kwargs)
        return context



class JobApplyView(CreateView):
    """
    Try to apply a job.
    """
    model = JobProposal
    fields = ('proposal',)
    template_name = 'jobs/job_apply_form.html'

    def get_context_data(self, **kwargs):
        kwargs['jobs'] = Job.objects.get(pk=self.kwargs.get('pk'))
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        proposal = form.save(commit=False)
        proposal.job = Job.objects.get(pk=self.kwargs.get('pk'))
        proposal.freelancer = self.request.user

        proposal.save()
        return redirect('users:job_profile', self.request.user.username)



class ProposalAcceptView(RedirectView):
    """
    Aceept a proposal.
    """
    permanent = False
    query_string = True
    pattern_name = 'jobs:job_detail'

    def get_redirect_url(self, *args, **kwargs):
        job = get_object_or_404(Job, pk=kwargs['pk'])
        job.freelancer = User.objects.get(username=kwargs.get('username'))
        job.status = 'working'
        job.save()

        return super().get_redirect_url(*kwargs, pk=kwargs['pk'])



