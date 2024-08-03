import time


class CurrentTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print(time.strftime("%H:%M:%S"))
        response = self.get_response(request)

        return response
