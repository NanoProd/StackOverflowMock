from flask.templating import render_template
from project import create_app


app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
