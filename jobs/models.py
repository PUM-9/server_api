from django.db import models
from enum import Enum
from django.utils import timezone
from users.models import User
from web_application.settings import FILE_UPLOAD_DIR
import random
import string
import os


def randomword(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


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
    log_level = models.SmallIntegerField('log_level', default=LogLevel.WARNING)
    name = models.CharField('name', max_length=200)


class Registration(Job):
    max_correspondence = models.FloatField('max_correspondence')
    max_iterations = models.IntegerField('max_iterations')
    transformation_epsilon = models.FloatField('transformation_epsilon')
    leaf_size = models.FloatField('leaf_size')

    @classmethod
    def create(cls, name, log_lvl, max_corr, max_it, trans_eps, leaf_size):
        created = timezone.now()
        try:
            log_lvl = int(log_lvl)
        except ValueError:
            log_lvl = LogLevel.INFO
        registration = cls(name=name, created=created, log_level=log_lvl, max_correspondence=max_corr, max_iterations=max_it,
                           transformation_epsilon=trans_eps, leaf_size=leaf_size)
        registration.save()
        return registration.id


class Mesh(Job):
    pass


class File(models.Model):
    name = models.CharField('name', max_length=20)
    created = models.DateTimeField('created')
    path = models.CharField('path', max_length=300)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)

    @classmethod
    def create(cls, file, job_id):
        name = randomword(15)
        while File.objects.all().filter(name=name).len() > 0:
            name = randomword(15)
        name += ".pcd"
        created = timezone.now()
        if file.name.split('.').len() > 1 and file.name.split('.')[-1] == "pcd":
            path = os.path.join(FILE_UPLOAD_DIR, name)
            os.rename(file.path, path)
        else:
            return False
        db_file = cls(name=name, created=created, path=path, job_id=job_id)
        db_file.save()
        return True
