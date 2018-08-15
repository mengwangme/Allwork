from django.db import models

from taggit.managers import TaggableManager


class Job(models.Model):
    """
    Model to create a Job.

    Attributes:
        date_created (datetime): Datetime of job creation
        date_modified (datetime): Datetime of job modified
        document (file): Job description file
        freelancer (user):  Freelancer whom the job assigned.
        job_description (str): Job description
        job_title (str): Job title
        owner (user): User who owns the job
        price (decimal): Job price
        status (str): Job current status
        tags (str): Tags representing job

    """
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='job_owner'
    )
    freelancer = models.ForeignKey(
        'users.User',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="job_freelancer"
    )

    job_title = models.CharField(max_length=300)
    job_description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    tags = TaggableManager()

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    document = models.FileField(upload_to='attachements', blank=True, null=True)

    ACTIVE = 'active'
    WORKING = 'working'
    ENDED = 'ended'
    CHOICES = ((ACTIVE, 'active'), (WORKING, 'working'), (ENDED, 'ended'))

    status = models.CharField(max_length=9, choices=CHOICES, default=ACTIVE)

    class Meta:
        verbose_name = 'job'
        verbose_name_plural = 'jobs'
        unique_together = ('owner', 'date_created')

    def __str__(self):
        return "%s - %s - %s" % (
            self.owner.get_full_name(),
            self.freelancer.get_full_name() if self.freelancer else '',
            self.status
        )

    @property
    def freelancers(self):
        """
        It prepares all the freelancers of the current job.
        """
        proposals = self.job_proposal.all()
        return  [proposal.freelancer for proposal in proposals]

class JobProposal(models.Model):
    """
    Model to create a freelancers's proposal for a JOB.

    Attributes:
        freelancer (user): User who submits job proposal
        job (job): Job object
        proposal (text): User proposal for the job
    """
    job = models.ForeignKey(
        'Job',
        on_delete=models.CASCADE,
        related_name="proposal_job",
    )
    freelancer = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="proposal_freelancer",
    )

    proposal = models.TextField()

    class Meta:
        unique_together = ('job', 'freelancer')
