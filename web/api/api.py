import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/user/address', methods=['GET'])
def api_user_address():
    return "<h1>User address</h1><p>This site is a prototype API for the user address.</p>"


@app.route('/', methods=['GET'])
def home():
    return "<h1>Central API</h1><p>This site is a prototype central API.</p>"


if __name__ == "__main__":
    app.run()