from sparrow import Sparrow
from httpserver import HttpResponse


def index(request):
    response = HttpResponse()
    response.set_body('hey man!')
    response.set_cookie('aaa', '111', 10)
    return response.get_response()


routes = [
    (r'^/index$', index)
]


app = Sparrow(routes)
app.run(port=6666)
