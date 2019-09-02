# coding=utf-8

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from common.models import DeleteStatusMixin, GmtCreateModifiedTimeMixin


SEX = (
    (0, "未知"),
    (1, "女"),
    (2, "男"),
)

class MyUserManager(BaseUserManager):
    def create_user(self, phone, name, password=None):
        """
        Creates and saves a User with the given phone, date of
        birth and password.
        """

        if not phone:
            raise ValueError('Users must have a phone number')

        user = self.model(
            # email=self.normalize_email(email),
            name=name,
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password):
        """
        Creates and saves a superuser with the given phone, date of
        birth and password.
        """
        user = self.create_user(
            phone=phone,
            # email=email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin, GmtCreateModifiedTimeMixin):
    nick_name = models.CharField(verbose_name="用户昵称", max_length=64, null=True, blank=True, unique=True)
    real_name = models.CharField(verbose_name="真实姓名", max_length=64, null=True, blank=True)
    pic = models.CharField(verbose_name="头像", max_length=255, null=True, blank=True)
    sex = models.IntegerField(verbose_name="性别", choices=SEX, default=0)
    birth_date = models.DateTimeField(verbose_name="出生年月", null=True, blank=True)
    email = models.EmailField(verbose_name='用户邮箱', max_length=100, null=True, blank=True, unique=True)
    pay_password = models.CharField(verbose_name='支付密码', max_length=64, null=True, blank=True)
    user_mobile = models.CharField(verbose_name='手机号码', max_length=64, null=True, blank=True, unique=True)
    user_regip = models.CharField(verbose_name='注册IP', max_length=64, null=True, blank=True)
    user_lastip = models.CharField(verbose_name='最后登录IP', max_length=64, null=True, blank=True)
    user_memo = models.CharField(verbose_name='备注', max_length=64, null=True, blank=True)
    score = models.IntegerField(verbose_name='用户积分', null=False, default=0)

    openid = models.CharField(verbose_name='openid', blank=True, null=True, max_length=32, unique=True)
    unionid = models.CharField(verbose_name='unionid', blank=True, null=True, max_length=20)
    provider = models.CharField(verbose_name='用户来源', max_length=32, null=True, blank=True)

    is_active = models.BooleanField(verbose_name='是否删除', default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'nick_name'
    REQUIRED_FIELDS = ['openid']

    def __str__(self):
        return self.nick_name

    @property
    def is_staff(self):
        """ Is the user a member of staff? """
        # Simplest possible answer: All admins are staff
        return self.is_admin
