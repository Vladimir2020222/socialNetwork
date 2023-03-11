from django.db import connection
from django.db.backends.base.base import BaseDatabaseWrapper

connection: BaseDatabaseWrapper


class QueriesManager:
    def __init__(self):
        self.show_time = False

    @property
    def last(self):
        return self[-1]

    def __getitem__(self, item):
        queries = self.queries[item]
        return queries

    @property
    def queries(self):
        return connection.queries if self.show_time else [i['sql'] for i in connection.queries]

    def __repr__(self):
        for i in self.queries:
            i = i.replace('"', '')
            print(i)
        return ''

    def __len__(self):
        return len(self.queries)

    def clear(self):
        connection.queries_log.clear()

    __str__ = __repr__


q = QueriesManager()
