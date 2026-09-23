from flask import Flask, request, session, redirect


def auth():
    if request.path.startswith("/static"):  # 放行静态资源
        return None
    if request.path == "/home":
        return None
    if request.path == "/login":
        return None
    else:
        user_info = session.get("user_info")
        if user_info:
            return None
        else:
            return redirect("/home")


def create_app():
    app = Flask(__name__)
    app.secret_key = "dsaihnqbnsadnahxqwnpi"
    from .views import account
    from .views import order
    app.register_blueprint(account.ac)
    app.register_blueprint(order.od)
    app.before_request(auth)
    return app
