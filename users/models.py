from taggit.managers import TaggableManager # ????????

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

class UserManager(BaseUserManager):

    def create_user(self, username, email, password, **kwargs):
        if not email:
            raise ValueError("Users must have a valid email address.")

		 # ??????????
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            first_name = kwargs.get('first_name'),
            last_name=kwargs.get('last_name'),
        )
		# ???????hash??
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None, **kwargs):
        """
        ??????
        """

        # ???????
        user = self.create_user(
            username, email, password, **kwargs
        )

		 # ??????????
        user.is_admin = True	# ???
        user.is_superuser = True	# ????
        user.is_staff = True	# ??
        user.save()

        return user



class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True) # ???????

    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    # ???????????????
    profile_photo = models.ImageField(upload_to='pic_folder', default='pic_folder/default.jpg')
    profile = models.TextField(null=True, blank=True)
    skills = TaggableManager(blank=True)

    # ????????????/??
    is_owner = models.BooleanField('project_owner status', default=False)
    is_freelancer = models.BooleanField('freelancer status', default=False)

    date_created = models.DateTimeField(auto_now_add=True) # ??????
    date_modified = models.DateTimeField(auto_now=True) # ??????

    is_admin = models.BooleanField(default=False) # ?????????????True?
    is_superuser = models.BooleanField(default=False) # ?????????????True?
    is_staff = models.BooleanField(default=False) # ???????????????? True?
    is_active = models.BooleanField(default=True) # ?????????????????True?

    objects = UserManager()	# ?????manager

    USERNAME_FIELD = 'username' # ????????????????????????
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name'] # ??createsuperuser????????????????????

	 # ???admin???????
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

	# ??????
    def get_short_name(self):
        return self.first_name

	# ????
    def get_full_name(self):
        if self.first_name:
            first_name = ' '.join(
                [i.capitalize() for i in self.first_name.split(' ')]
            )
            last_name = ' '.join(
                [i.capitalize() for i in self.last_name.split(' ')
                 if self.last_name]
            )
            full_name = [first_name, last_name]
            full_name = ' '.join(
                [i.strip() for i in full_name if i.strip()]
            )

            return full_name
        else:
            return "%s" % (self.email)

	# ???????????jobs??????jobs???????????jobs
    # @property
    # def income(self):
    #     """
    #     ???????????????????
    #     """
    #     completed_jobs = self.job_freelancer.filter(status="ended")
	#
    #     income = 0
    #     for job in completed_jobs:
    #         income += job.price
	#
    #     return income


