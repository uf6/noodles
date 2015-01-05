from noodles.core import app


@app.route('/')
def index():
    return 'hello, world!'
