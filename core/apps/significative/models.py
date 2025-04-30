from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Service(models.Model):
    # Модель услуги/сервиса, который на можно записаться
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    description = models.TextField(blank=True, verbose_name="Описание")
    duration = models.DurationField(verbose_name="Продолжительность")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class Specialist(models.Model):
    # Модель специалиста, оказывающего услуги
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='specialist')
    services = models.ManyToManyField(Service, related_name='specialists')
    bio = models.TextField(blank=True, verbose_name="О специалисте")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return f"{self.user.get_full_name()}"

    class Meta:
        verbose_name = "Специалист"
        verbose_name_plural = "Специалисты"


class Schedule(models.Model):
    # Расписание специалиста
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField(verbose_name="Дата")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")
    is_available = models.BooleanField(default=True, verbose_name="Доступно")

    def __str__(self):
        return f"{self.specialist} - {self.date} {self.start_time}-{self.end_time}"

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"
        unique_together = ('specialist', 'date', 'start_time', 'end_time')


class Appointment(models.Model):
    # Запись на прием
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='appointments')
    start_time = models.DateTimeField(verbose_name="Время начала")
    end_time = models.DateTimeField(verbose_name="Время окончания")
    STATUS_CHOICES = [
        ('booked', 'Забронировано'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
        ('no_show', 'Не явился'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    notes = models.TextField(blank=True, verbose_name="Примечания")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.client} -> {self.specialist} ({self.service}) {self.start_time}"

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ['-start_time']


class Holiday(models.Model):
    # Выходные/праздничные дни специалиста
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='holidays')
    date = models.DateField(verbose_name="Дата")
    reason = models.CharField(max_length=255, blank=True, verbose_name="Причина")

    def __str__(self):
        return f"{self.specialist} - {self.date}"

    class Meta:
        verbose_name = "Выходной день"
        verbose_name_plural = "Выходные дни"
        unique_together = ('specialist', 'date')


class ScheduleTemplate:
    pass