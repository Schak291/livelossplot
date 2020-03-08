import neptune

from livelossplot.main_logger import MainLogger
from livelossplot.output_plugins.base_output import BaseOutput


class NeptuneLogger(BaseOutput):
    """See: https://github.com/neptune-ai/neptune-client
    YOUR_API_TOKEN and USERNAME/PROJECT_NAME
    """

    def __init__(self, api_token: str, project_qualified_name: str):
        self.neptune = neptune
        self.neptune.init(api_token=api_token, project_qualified_name=project_qualified_name)
        self.neptune.create_experiment()

    def close(self):
        self.neptune.stop()

    def send(self, logger: MainLogger):
        for name, log_items in logger.log_history.items():
            last_log_item = log_items[-1]
            self.neptune.send_metric(name, last_log_item.value)
            self.neptune.send_metric(name, y=last_log_item.value, x=last_log_item.step)
