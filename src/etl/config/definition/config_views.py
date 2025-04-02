from config.utils.work_view import WorkView
from core.env.env import Env

from config.definition.views.dataset_ai_view import DatasetAiView


class ConfigViews(WorkView):
    def __init__(self, env: Env):
        super().__init__([DatasetAiView(env)])