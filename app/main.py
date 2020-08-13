import flask
from . import cli
app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/api/survey')
def survey():
    conn = psycopg2.connect(settings.DB_URL)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title FROM Surveys WHERE id= %s", [1])
    finally:
        conn.close()


@app.cli.command("init-db")
def init_db():
    """Create Schema and load test data."""
    return cli.init_db()
