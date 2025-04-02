from abc import ABC, abstractmethod


class DefineView(ABC):
    @abstractmethod
    def get_select(self) -> str :
        return ""



class View:
    def __init__(self, name: str, select: str | None, define_view: DefineView):
        self.name = name
        self.select = select
        self.define_view = define_view
        pass

    def get_query_to_create(self):
        select = self.define_view.get_select() if self.select is None else self.select
        return f"""
                    CREATE VIEW {self.name} AS {select}
                """
    def get_query_to_delete(self):
        return f"""
                    DELETE VIEW IF EXISTS {self.name}
                """