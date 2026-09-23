from flask import Blueprint, session, render_template, request, redirect
from utils import db
from utils import cache
from utils.db import execute

# 蓝图对象
od = Blueprint("order", __name__)


@od.route("/order/list")
def order_list():
    user_id = session["user_info"]["id"]
    vip_info = db.fetch_one("select * from vip where id=%s",
                            [user_id])
    vip_rank = vip_info["rank"]
    user_info = session.get("user_info")
    role = user_info["role"]
    if role == 1:
        datalist = db.fetch_all("""
                    SELECT DISTINCT o.*, u.user_name 
                    FROM `order` o 
                    LEFT JOIN user_info u ON o.user_id = u.id
                """, [])
    else:
        datalist = db.fetch_all("""
                    SELECT DISTINCT o.*, u.user_name 
                    FROM `order` o 
                    LEFT JOIN user_info u ON o.user_id = u.id 
                    WHERE o.user_id = %s
                """, [user_info['id']])
    status_dict = {
        1: "待执行",
        2: "正在执行",
        3: "完成",
        4: "失败"
    }
    return render_template("order_list.html", datalist=datalist, status_dict=status_dict, vip_rank=vip_rank)


@od.route("/order/create", methods=["GET", "POST"])
def create_order():
    if request.method == "GET":
        return render_template("create_order.html")
    cyber_os = request.form.get("cyber_os")  # 方便演示 只获取了操作系统的数据写入到数据库
    num_os = request.form.get("num_os", type=int)

    # 写入数据库
    user_info = session.get("user_info")
    params = [cyber_os, num_os, user_info["id"]]
    order_id = db.create("insert into `order`(cyberware,count,user_id,status)values(%s,%s,%s,1)", params)

    # 写入redis队列
    cache.push(order_id)
    return redirect("/order/list")


@od.route("/order/delete")
def delete_order():
    order_id = request.args.get("order_id", type=int)

    if not order_id:
        return redirect("/order/list")

    execute("DELETE FROM `order` WHERE order_id=%s", [order_id])

    return redirect("/order/list")
