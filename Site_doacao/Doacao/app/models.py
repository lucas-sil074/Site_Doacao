from django.db import models

class Doador(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    tipo_sanguineo = models.CharField(max_length=3, choices=[
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ])
    data_nascimento = models.DateField()

    def __str__(self):
        return self.nome

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    tipo_sanguineo = models.CharField(max_length=3, choices=[
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ])
    necessidade = models.TextField()

    def __str__(self):
        return self.nome

