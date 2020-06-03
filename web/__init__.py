from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/test')
def test_page():
    # we can request /test with parameters as /test?param1=a&param2=b, etc.
    # we'll simply print them to show how
    # render template from test.html in directory templates (default)
    print('got', request.args)
    return render_template('test.html', data=list(request.args.items()))

def run(port: int):
    app.run(host='0.0.0.0', port=port)

