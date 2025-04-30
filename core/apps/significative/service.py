# services.py
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Schedule, Schedule


def generate_simple_slots(specialist, days_ahead=7):
    """
    Генерирует слоты расписания на указанное количество дней вперед
    """
    # Получаем активные шаблоны специалиста
    templates = Schedule(
        specialist=specialist,
        is_active=True
    )

    # Определяем даты для генерации
    today = timezone.now().date()
    end_date = today + timedelta(days=days_ahead)

    created_slots = 0

    # Генерируем слоты для каждого дня
    for day in range(days_ahead):
        current_date = today + timedelta(days=day)
        weekday = current_date.weekday()

        # Ищем шаблоны для текущего дня недели
        for template in templates.filter(day_of_week=weekday):
            slot_start = datetime.combine(current_date, template.start_time)
            slot_end = datetime.combine(current_date, template.end_time)

            # Создаем слоты с заданным интервалом
            while slot_start + timedelta(minutes=template.slot_duration) <= slot_end:
                Schedule(
                    specialist=specialist,
                    start_datetime=timezone.make_aware(slot_start),
                    end_datetime=timezone.make_aware(
                        slot_start + timedelta(minutes=template.slot_duration)
                    ),
                    is_available=True
                )
                created_slots += 1
                slot_start += timedelta(minutes=template.slot_duration)

    return created_slots