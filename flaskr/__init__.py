# contains the application factory
# tells python to treat this as package

import os
from flask import Flask

def create_app(test_config=None):
    # instance_relative_config tells that config are relative to the instance
    app = Flask(__name__, instance_relative_config=True)
    # it is name of the package
    print(__name__) # flaskr
    # 'instance' next to the package or module is assumed to be the instance path.
    # i.e in this case flaskr is assumed to be the instance path.
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load test_config if passed in
        app.config.from_mapping(test_config)

    # ensures that instance folder exists as
    # sqlite file exists at the app instance
    try:
        # new instance directory is created for app
        print(app.instance_path) # F:\btech_books\web_works\flask-tutorial\instance
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # simple application
    @app.route('/hello')
    def hello():
        return 'hello!'

    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)

    return app