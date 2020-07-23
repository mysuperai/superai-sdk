from superai.apis.task_instance import TaskInstance
from superai.apis.task_template import TaskTemplate

class Task(TaskTemplate):

    def __call__(self, *args, quality=None, cost=None, latency=None, **kwargs):
        instance = TaskInstance(self.template_id, quality=quality, cost=cost, latency=latency, **kwargs)
        return instance



