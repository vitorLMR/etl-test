from config.utils.work_view import WorkView

from config.definition.views.dataset_ai_view import DatasetAiView

class ConfigViews(WorkView):
    def __init__(self):
        super.__init__([DatasetAiView()])
        pass