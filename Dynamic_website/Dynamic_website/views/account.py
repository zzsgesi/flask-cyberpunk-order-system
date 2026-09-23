from flask import Blueprint, render_template, request, redirect, session
from utils import db

# 蓝图对象
ac = Blueprint("account", __name__)


@ac.route("/home")
def home():
    return render_template("home.html")


@ac.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    role = request.form.get("role")
    account = request.form.get("account")
    password = request.form.get("password")
    # 连接数据库
    users_dict = db.fetch_one("select * from user_info where role=%s and account=%s and password=%s",
                              [role, account, password])

    # 进行校验
    if users_dict:
        # 登录成功 + 跳转
        session["user_info"] = {"role": users_dict["role"], "user_name": users_dict["user_name"],
                                "id": users_dict["id"]}
        return redirect("/introduction")
    else:
        return render_template("login.html", error="用户名或密码错误，检查权限是否正确")


@ac.route("/introduction")
def introduction():
    user_id = session["user_info"]["id"]
    vip_info = db.fetch_one("select * from vip where id=%s",
                            [user_id])
    vip_rank = vip_info["rank"]
    return render_template("introduction.html", vip_rank=vip_rank)
