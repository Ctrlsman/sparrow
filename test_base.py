from sparrow import Sparrow
from httpserver import HttpResponse


def index(request):
    response = HttpResponse()
    response.set_body('hey man!')
    return response.get_response()


routes = [
    (r'/index^', index)
]


app = Sparrow(routes)
app.run(port=6666)
