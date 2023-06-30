from django.db import models


class Call(models.Model):
    msisdn = models.CharField(max_length=255)
    dialed = models.CharField(max_length=255)
    start_time = models.CharField(max_length=255)
    duration = models.IntegerField()
    circuit_in = models.CharField(max_length=255)
    circuit_out = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    file_index = models.IntegerField()

    def __str__(self):
        return f"Call {self.pk}"


class Volume(models.Model):
    file_index = models.IntegerField()
    prefix_zones = models.CharField(max_length=255)
    duration = models.IntegerField()

    def __str__(self):
        return f"Volume {self.pk}"
