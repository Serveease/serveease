from flask import Flask

def create_app():
    app = Flask(__name__)

    # Optional: register blueprints, config, routes here
    @app.route("/")
    def home():
        return "Hello from Flask on Render!"

    return app
