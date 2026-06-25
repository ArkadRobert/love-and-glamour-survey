from flask import Flask, render_template, request, redirect
from urllib.parse import quote
import sqlite3

app = Flask(__name__)

app.config["SECRET_KEY"] = "love-glamour-secret-key"


def get_db_connection():
    conn = sqlite3.connect("orders.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        recipient_name TEXT,
        recipient_phone TEXT,
        service TEXT NOT NULL,
        package TEXT NOT NULL,
        delivery_date TEXT,
        delivery_time TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


create_table()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/order", methods=["GET", "POST"])
def order():

    if request.method == "POST":

        customer_name = request.form.get("customer_name")
        phone = request.form.get("phone")

        recipient_name = request.form.get("recipient_name")
        recipient_phone = request.form.get("recipient_phone")

        service = request.form.get("service")
        package = request.form.get("package")

        delivery_date = request.form.get("delivery_date")
        delivery_time = request.form.get("delivery_time")

        message = request.form.get("message")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO orders (
            customer_name,
            phone,
            recipient_name,
            recipient_phone,
            service,
            package,
            delivery_date,
            delivery_time,
            message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            customer_name,
            phone,
            recipient_name,
            recipient_phone,
            service,
            package,
            delivery_date,
            delivery_time,
            message
        ))

        conn.commit()
        conn.close()

        whatsapp_message = f"""
NEW ORDER

Customer: {customer_name}
Phone: {phone}

Recipient: {recipient_name}
Recipient Phone: {recipient_phone}

Service: {service}
Package: {package}

Date: {delivery_date}
Time: {delivery_time}

Message:
{message}
"""

        whatsapp_url = (
            "https://wa.me/2347082514967?text="
            + quote(whatsapp_message)
        )

        return redirect(whatsapp_url)

    return render_template("order.html")


@app.route("/admin")
def admin():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM orders
    ORDER BY id DESC
    """)

    orders = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        orders=orders
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )


