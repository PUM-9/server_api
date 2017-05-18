from django.db import models
from enum import Enum
from django.utils import timezone
from users.models import User
from web_application.settings import FILE_UPLOAD_DIR
import random
import string
import os
import subprocess


def random_word(length):
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
        registration = cls(name=name, created=created, log_level=log_lvl, max_correspondence=max_corr,
                           max_iterations=max_it, transformation_epsilon=trans_eps, leaf_size=leaf_size)
        registration.save()
        return registration

    def execute(self):
        self.started = timezone.now()
        self.save()
        command = list(['3DCopy'])
        command.append('-r')
        command.append('-d ' + str(self.max_correspondence))
        command.append('-i ' + str(self.max_iterations))
        timeout = 5 * 60 * 60  # Timeout after 5 hours.
        try:
            subprocess.run(command, timeout=timeout, stdout=subprocess.PIPE)
        except subprocess.TimeoutExpired:
            self.finished = timezone.now()
            # Maybe add some error in the database so we can display it.
        except Exception:
            self.finished = timezone.now()
            # Add some other error in the database
        return

    def class_name(self):
        return self.__class__.__name__

class Mesh(Job):

    @classmethod
    def create(cls, name, log_lvl):
        created = timezone.now()
        try:
            log_lvl = int(log_lvl)
        except ValueError:
            log_lvl = LogLevel.INFO
        mesh = cls(name=name, created=created, log_level=log_lvl)
        mesh.save()
        return mesh

    def class_name(self):
        return self.__class__.__name__

class File(models.Model):
    name = models.CharField('name', max_length=20)
    created = models.DateTimeField('created')
    path = models.CharField('path', max_length=300)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    @classmethod
    def create_pcd(cls, uploaded_file, job):
        name = random_word(15)
        while len(File.objects.all().filter(name=name)) > 0:
            name = random_word(15)
        name += ".pcd"
        created = timezone.now()
        if len(uploaded_file.name.split('.')) > 1 and uploaded_file.name.split('.')[-1] == "pcd":
            path = os.path.join(FILE_UPLOAD_DIR, name)
            file = open(path, "wb")
            for chunk in uploaded_file.chunks():
                file.write(chunk)
            file.close()
        else:
            return False
        db_file = cls(name=name, created=created, path=path, job=job)
        db_file.save()
        return db_file
