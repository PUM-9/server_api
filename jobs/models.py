from django.db import models
from enum import Enum
from django.utils import timezone
from users.models import User


class LogLevel(Enum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4


class Job(models.Model):
    created = models.DateTimeField('created')
    started = models.DateTimeField('started', null=True)
    finished = models.DateTimeField('finished', null=True)
    job_type = models.CharField('job_type', max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    log_level = models.SmallIntegerField('log_level', default=LogLevel.WARNING)


class Registration(Job):
    max_correspondence = models.FloatField('max_correspondence')
    max_iterations = models.IntegerField('max_iterations')
    transformation_epsilon = models.FloatField('transformation_epsilon')
    leaf_size = models.FloatField('leaf_size')

    @classmethod
    def create_from_json(cls, arguments):
        print(arguments)


class Mesh(Job):
    pass


class File(models.Model):
    created = models.DateTimeField('created')
    path = models.CharField('path', max_length=300)
    file_type = models.CharField('file_type', max_length=100)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
