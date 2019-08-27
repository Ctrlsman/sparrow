from sparrow import Sparrow
from sparrow import HttpResponse


def index(request):
    return HttpResponse('hey man!')

routes = [
    (r'/index', index)
]


app = Sparrow(routes)
app.run(port=6666)


