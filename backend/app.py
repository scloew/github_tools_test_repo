from flask import Flask
from flask_cors import CORS

from movies.routes import movies
from members.routes import members
from cart.routes import cart
from rentals.routes import rentals

app = Flask(__name__)
app.register_blueprint(movies)
app.register_blueprint(members)
app.register_blueprint(cart)
app.register_blueprint(rentals)
CORS(app)


@app.route('/')
def index():
    return '<div> HELLO WORLD </div>'


if __name__ == '__main__':
    app.run(host="127.0.0.1", port="5000", debug=True)
