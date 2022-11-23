
from wsgiref.simple_server import make_server
# from schema import *

from app.user.views import *
from app.category.views import *
from app.producer.views import *
from app.drug.views import *
from app.cart.views import *
from app.order.views import *

if __name__ == "__main__":
    app.run(debug=True)
