from datetime import datetime, timedelta, timezone
from typing import TypedDict

from icalendar import Calendar, Event as ICalEvent
from croniter import croniter

from maxhack.core.ids import GroupId
from maxhack.core.utils.datehelp import UTC_TIMEZONE
from maxhack.database.models import EventModel, GroupModel


def generate_ics_for_events(
    events: list[EventModel],
    groups: dict[GroupId, GroupModel],
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> bytes:
    """Генерирует .ics файл для списка событий.

    Args:
        events: Список событий для экспорта
        groups: Словарь групп по group_id для получения названий групп
        start_date: Начальная дата для генерации повторяющихся событий (по умолчанию сегодня)
        end_date: Конечная дата для генерации повторяющихся событий (по умолчанию через год)

    Returns:
        bytes: Содержимое .ics файла
    """
    cal = Calendar()
    cal.add("prodid", "-//MaxHack Calendar//EN")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")
    cal.add("method", "PUBLISH")

    if start_date is None:
        start_date = datetime.now()
    if end_date is None:
        end_date = start_date + timedelta(days=365)

    # Фильтруем события, которые уже случились (для не повторяющихся)
    current_time = datetime.now(timezone.utc)

    for event in events:
        # Пропускаем события, которые уже случились и не повторяющиеся
        if event.event_happened and not event.is_cycle:
            continue
        group = groups.get(event.group_id)
        organizer_name = group.name if group else "Unknown Group"

        # Создаем timezone для события на основе timezone события (в минутах)
        event_tz_offset = timedelta(minutes=event.timezone)
        event_timezone = timezone(event_tz_offset)

        # Парсим cron выражение
        try:
            # Используем start_date с учетом timezone события
            event_start_date = start_date.replace(tzinfo=event_timezone)
            cron = croniter(event.cron, event_start_date)
        except Exception:
            # Если cron невалидный, пропускаем событие
            continue

        # Генерируем события на основе cron
        event_count = 0
        max_events = 1000  # Ограничение на количество событий
        last_date = None

        while event_count < max_events:
            try:
                next_date = cron.get_next(datetime)
                # Приводим к timezone события
                if next_date.tzinfo is None:
                    next_date = next_date.replace(tzinfo=event_timezone)
                else:
                    next_date = next_date.astimezone(event_timezone)

                if next_date > end_date.replace(tzinfo=event_timezone):
                    break

                # Проверяем, что не генерируем одно и то же событие дважды
                if last_date and next_date <= last_date:
                    break

                # Пропускаем события, которые уже в прошлом
                if next_date < current_time.replace(tzinfo=event_timezone):
                    continue

                # Создаем событие в календаре
                ical_event = ICalEvent()
                ical_event.add("summary", event.title)
                ical_event.add("dtstart", next_date)
                ical_event.add("dtstamp", datetime.now(timezone.utc))

                # Добавляем длительность
                if event.duration:
                    end_datetime = next_date + timedelta(minutes=event.duration)
                    ical_event.add("dtend", end_datetime)
                else:
                    # Если длительность не указана, событие длится 1 час
                    ical_event.add("dtend", next_date + timedelta(hours=1))

                # Описание
                if event.description:
                    ical_event.add("description", event.description)

                # Организатор (email оставляем пустым)
                ical_event.add("organizer", f"CN={organizer_name}:mailto:")

                # Location оставляем пустым (не добавляем поле)

                # UID для уникальности события
                ical_event.add(
                    "uid",
                    f"event-{event.id}-{int(next_date.timestamp())}@maxhack",
                )

                cal.add_component(ical_event)
                event_count += 1
                last_date = next_date

                # Если событие не повторяющееся, выходим после первого
                if not event.is_cycle:
                    break

            except Exception:
                # Если ошибка при генерации следующей даты, пропускаем
                break

    # Конвертируем календарь в bytes
    ics_bytes = cal.to_ical()
    return ics_bytes


class ParsedICSEvent(TypedDict):
    """Структура события, распарсенного из .ics файла."""

    title: str
    description: str | None
    date: datetime
    duration: int  # в минутах
    timezone: int  # offset в минутах от UTC
    every_day: bool
    every_week: bool
    every_month: bool


def parse_ics_file(ics_content: bytes) -> list[ParsedICSEvent]:
    """Парсит .ics файл и возвращает список событий для импорта.

    Args:
        ics_content: Содержимое .ics файла в формате bytes

    Returns:
        list[ParsedICSEvent]: Список распарсенных событий
    """
    events: list[ParsedICSEvent] = []
    try:
        cal = Calendar.from_ical(ics_content)
    except Exception:
        return events

    for component in cal.walk():
        if component.name != "VEVENT":
            continue

        try:
            # Извлекаем название
            summary = component.get("summary")
            if not summary:
                continue
            title = str(summary)

            # Извлекаем описание
            description = component.get("description")
            description_str = str(description) if description else None

            # Извлекаем дату начала
            dtstart = component.get("dtstart")
            if not dtstart:
                continue

            start_dt = dtstart.dt
            if isinstance(start_dt, datetime):
                # Если есть timezone, используем его
                if start_dt.tzinfo:
                    # Конвертируем timezone в offset в минутах от UTC
                    utc_offset = start_dt.utcoffset()
                    if utc_offset:
                        timezone_offset_minutes = int(utc_offset.total_seconds() / 60)
                    else:
                        timezone_offset_minutes = 0
                    # Приводим к UTC для хранения
                    start_dt = start_dt.astimezone(UTC_TIMEZONE)
                else:
                    # Если timezone нет, считаем что время в локальном timezone (по умолчанию UTC)
                    timezone_offset_minutes = 0
                    start_dt = start_dt.replace(tzinfo=UTC_TIMEZONE)
            else:
                # Если это date без времени, конвертируем в datetime
                start_dt = datetime.combine(start_dt, datetime.min.time())
                start_dt = start_dt.replace(tzinfo=UTC_TIMEZONE)
                timezone_offset_minutes = 0

            # Извлекаем дату окончания для вычисления duration
            dtend = component.get("dtend")
            duration_minutes = 60  # По умолчанию 1 час
            if dtend:
                end_dt = dtend.dt
                if isinstance(end_dt, datetime):
                    if end_dt.tzinfo:
                        end_dt = end_dt.astimezone(UTC_TIMEZONE)
                    else:
                        end_dt = end_dt.replace(tzinfo=UTC_TIMEZONE)
                    duration_delta = end_dt - start_dt
                    duration_minutes = int(duration_delta.total_seconds() / 60)
                    # Если duration отрицательный или нулевой, устанавливаем 1 час
                    if duration_minutes <= 0:
                        duration_minutes = 60

            # Определяем повторяемость из RRULE
            every_day = False
            every_week = False
            every_month = False

            rrule = component.get("rrule")
            if rrule:
                freq = rrule.get("FREQ")
                if freq:
                    freq_str = str(freq).upper()
                    if freq_str == "DAILY":
                        every_day = True
                    elif freq_str == "WEEKLY":
                        every_week = True
                    elif freq_str == "MONTHLY":
                        every_month = True
                    # Другие частоты (YEARLY и т.д.) игнорируем, создаем разовое событие

            events.append(
                {
                    "title": title,
                    "description": description_str,
                    "date": start_dt,
                    "duration": duration_minutes,
                    "timezone": timezone_offset_minutes,
                    "every_day": every_day,
                    "every_week": every_week,
                    "every_month": every_month,
                },
            )

        except Exception:
            # Пропускаем события, которые не удалось распарсить
            continue

    return events

