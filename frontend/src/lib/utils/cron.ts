import parser from 'cron-parser'
import type { EventResponse } from '../api/gen.schemas'

export function expandCronEvents(
  events: Array<EventResponse>,
  startDate: Date,
  endDate: Date,
) {
  const result = []

  for (const ev of events) {
    try {
      const offsetHours = ev.timezone / 60

      const options = {
        currentDate: startDate,
        endDate,
        iterator: true,
        tz: `Etc/GMT${offsetHours > 0 ? '-' : '+'}${Math.abs(offsetHours)}`,
      }

      const interval = parser.parse(ev.cron, options)

      // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
      while (true) {
        try {
          const obj = interval.next()
          result.push({
            id: ev.id,
            title: ev.title,
            date: obj.toDate(),
            type: ev.type === 'message' ? 'message' : 'event',
          })
        } catch {
          break
        }
      }
    } catch (err) {
      console.error('Error expanding cron events:', err)
    }
  }

  return result.sort((a, b) => a.date.getTime() - b.date.getTime())
}
