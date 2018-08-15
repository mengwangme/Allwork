from taggit.managers import TaggableManager

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

class UserManager(BaseUserManager):

    def create_user(self, username, email, password, **kwargs):
        """
        Create and save a User.

        :param username: username used by the user.
        :param email: email_id used by the user.
        :param password: password used by the user.
        :param kwargs: contaitns dictionary other user fields.
        :return: current created user.
        """
        if not email:
            raise ValueError("Users must have a valid email address.")

        user = self.model(
            username = username,
            email = self.normalize_email(email),
            first_name = kwargs.get('first_name'),
            last_name=kwargs.get('last_name'),
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None, **kwargs):
        """
        Create and save a superuser User.

        Used for `python manage.py createsuperuser`.

        :param username: username used by the superuser.
        :param email: email_id used by the superuser.
        :param password: password used by the superuser.
        :param kwargs: contaitns dictionary other superuser fields.
        :return: current created superuser.
        """

        # create default data for superuser
        user = self.create_user(
            username, email, password, **kwargs
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model to create User.

    :id: User id.
    :username: Username of the user.
    :email: User email.
    :first_name: User first name.
    :last_name: User last name.
    :user_type: Whether the User is a parent or a sitter.
    :date_created: User creation date.
    :date_modified: User modified date.
    :is_admin: Whether or not the User is of admin status.
    :is_superuser: Whether or not the User is of superuser status.
    :is_staff: Whether or not the User is of staff status.
    """

    email = models.EmailField(unique=True)

    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    # 可修改部分
    profile_photo = models.ImageField(upload_to='pic_folder', default='pic_folder/default.jpg')
    profile = models.TextField(null=True, blank=True)
    skills = TaggableManager(blank=True)

    # 角色
    is_owner = models.BooleanField('project_owner status', default=False)
    is_freelancer = models.BooleanField('freelancer status', default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False) # 如果用户具有所有权限，值为True。
    is_superuser = models.BooleanField(default=False) # 如果用户具有所有权限，值为True。
    is_staff = models.BooleanField(default=False) # 如果用户被允许访问管理界面，值为 True。
    is_active = models.BooleanField(default=True) # 如果用户帐户当前处于活动状态，值为True。

    objects = UserManager()

    USERNAME_FIELD = 'username' # 描述用户模型上用作唯一标识符的字段名称的字符串。
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name'] # 通过createsuperuser管理命令创建用户时将提示的字段名称列表。

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def get_short_name(self):
        return self.first_name

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

    # @property
    # def income(self):
    #     """
    #     计算自由职业者的所有完成任务的总收入。
    #     """
    #     completed_jobs = self.job_freelancer.filter(status="ended")
    #
    #     income = 0
    #     for job in completed_jobs:
    #         income += job.price
    #
    #     return income

