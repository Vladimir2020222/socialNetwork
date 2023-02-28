from django.db import connection


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
            print(i)
        return ''

    def __len__(self):
        return len(self.queries)

    __str__ = __repr__


q = QueriesManager()
