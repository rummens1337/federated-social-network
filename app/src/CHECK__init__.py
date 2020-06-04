# from web.api.central import register_blueprints as api_central_blueprints
# from web.api.data import register_blueprints as api_data_blueprint

from flask import Flask, render_template, request, Blueprint

from web.api import api_central_blueprints, api_data_blueprint

app = Flask(__name__)


@app.route('/test')
def test_page():
    # we can request /test with parameters as /test?param1=a&param2=b, etc.
    # we'll simply print them to show how
    # render template from test.html in directory templates (default)
    print('got', request.args)
    return render_template('test.html', data=list(request.args.items()))

def run(port: int, server_type: str):
    if server_type == 'central':
        api_central_blueprints(app)
    elif server_type == 'data':
        api_data_blueprint(app)
    else:
        raise ValueError('Server type not supported.')
    print(app.url_map)
    app.run(host='0.0.0.0', port=port)

