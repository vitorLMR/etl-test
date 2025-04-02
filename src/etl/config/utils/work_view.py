from config.utils.view import View

class WorkView:
    def __init__(self, views: list[View]):
        self.__views = views
        pass

    def get_views(self) -> list[View]:
        return self.__views