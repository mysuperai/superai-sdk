from superai.apis.dp_instance import DataProgramInstance
from superai.apis.dp_template import DataProgramTemplate

class DataProgram(DataProgramTemplate):

    def __call__(self, *args, quality=None, cost=None, latency=None, **kwargs):
        instance = DataProgramInstance(self.template_id, quality=quality, cost=cost, latency=latency, **kwargs)
        return instance



