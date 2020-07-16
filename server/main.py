import flask

app = flask.Flask("__main__")

@app.route("/")
def my_index():
    return flask.render_template("index.html", token="SHOOORYUKEN")

@app.route("/app/<literal>")
def login_redirect(literal):
    token = []
    for l in literal.split("&"):
        token.append(l)
        # for var, tok in l.split("="):
        #     eval(f'{var}="{tok}"')
    return flask.render_template("index.html", token=literal, refresh="")

app.run(debug=True)