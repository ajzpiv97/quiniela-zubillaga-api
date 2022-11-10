from flask.cli import FlaskGroup
from flaskr.app import create_app
from flaskr.utils.extensions import migrate, db

app = create_app()
cli = FlaskGroup(app)


@cli.command("db")
def run_migration():
    migrate.init_app(app, db)


if __name__ == '__main__':
    cli()
