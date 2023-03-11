from time import time

from django.core.exceptions import MiddlewareNotUsed
from django.db import connection

from q import q


times = []


def debug_sql_wrapper(execute, sql, params, many, context):
    execute(sql, params, many, context)


class DebugMiddleware:
    def __init__(self, get_response):
        raise MiddlewareNotUsed()
        self.get_response = get_response

    def __call__(self, request):
        global times

        start = time()
        with connection.execute_wrapper(debug_sql_wrapper):
            response = self.get_response(request)
        end = time()

        print(q)

        time_spent = end - start
        times.append(time_spent)
        print(f'\nTOTAL {len(q)} queries; '
              f'spent {time_spent} seconds; '
              f'middle time is {sum(times)/len(times)}'
              )
        q.clear()
        return response
