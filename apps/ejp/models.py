from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class EJP(models.Model):
    n1 = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    n2 = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    n3 = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    n4 = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    n5 = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    p1 = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    p2 = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    my = models.BooleanField(default=0)
    won = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    date = models.DateField(blank=False, null=False)
