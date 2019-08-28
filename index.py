from flask import Flask, render_template, request, make_response
from werkzeug.middleware.proxy_fix import ProxyFix
import io

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        header = f.readline().decode("utf-8")
        if len(header.split(";")) == 1:
            return 'file is not semi-colon separated'
        result = ""
        for l in f:
            result += "\"" + \
                "\",\"".join(l.decode("utf-8").split(";")).strip() + "\"\n"
        output = make_response(result)
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output

    if request.method == 'GET':
        return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)
