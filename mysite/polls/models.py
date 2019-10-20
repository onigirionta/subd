from django.db import models

class Futures(models.Model):
    class Meta:
        db_table = 'zb'

    name = models.CharField(primary_key=True, max_length=20)
    base = models.CharField(max_length=20)
    exec_date = models.DateField()

class Trades(models.Model):
    class Meta:
        db_table = 'f_zb'
        unique_together = (('name', 'torg_date'),)
            
    name = models.CharField(primary_key=True, max_length=20)
    torg_date = models.DateField()
    day_end = models.DateField()
    quotation = models.DecimalField(max_digits=5, decimal_places=2)
    max_quot = models.DecimalField(max_digits=5, decimal_places=2)
    min_quot = models.DecimalField(max_digits=5, decimal_places=2)
    num_contr = models.IntegerField()

class Report(models.Model):
    class Meta:
        db_table = 'calc'
        unique_together = (('name', 'torg_date'),)

    name = models.CharField(primary_key=True, max_length=20)
    quotation = models.DecimalField(max_digits=5, decimal_places=2)
    torg_date = models.DateField()
    rk = models.FloatField()
    xk = models.FloatField()

class Summary(models.Model):
    name = models.CharField(primary_key=True, max_length=20)
    avg = models.FloatField()
    stddev = models.FloatField()
    variance = models.FloatField()
    min = models.FloatField()
    max = models.FloatField()
    count = models.IntegerField()
    normal = models.TextField()
        
