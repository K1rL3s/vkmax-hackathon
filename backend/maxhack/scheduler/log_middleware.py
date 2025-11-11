from taskiq import TaskiqMessage, TaskiqMiddleware

from maxhack.logger.bot.context_vars import (
    current_extra_data,
    current_task_id,
    current_task_name,
)


class ContextVarsMiddleware(TaskiqMiddleware):
    def pre_execute(self, message: TaskiqMessage) -> TaskiqMessage:
        current_task_id.set(message.task_id)
        current_task_name.set(message.task_name)
        current_extra_data.set(message.kwargs)
        return message
