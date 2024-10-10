from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import psycopg2.extras

views = Blueprint("views", __name__)


def get_db_connection():
    conn_str = "host=127.0.0.1 dbname=socketio user=postgres password=5599 port=5432"
    conn = psycopg2.connect(conn_str)
    return conn


@views.route("/")
def home():
    # if "loggedin" in session:
        return render_template("home.html")
    # , username=session["username"])
    # return redirect(url_for("auth.login"))


@views.route("/index")
def index():
    if "loggedin" in session:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM students")
        list_users = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("index.html", list_users=list_users)
    return redirect(url_for("auth.login"))


@views.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            cur.execute(
                "INSERT INTO students (fullname, username, email, password) VALUES (%s, %s, %s, %s)",
                (fullname, username, email, password),
            )
            conn.commit()
            flash("Student added successfully!")
            return redirect(url_for("views.index"))
        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}")
        finally:
            cur.close()
            conn.close()

    return render_template("add_student.html")


@views.route("/edit/<int:id>", methods=["GET", "POST"])
def get_student(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == "POST":
        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            cur.execute(
                """
                UPDATE students
                SET fullname = %s, username = %s, email = %s, password = %s
                WHERE id = %s
            """,
                (fullname, username, email, password, id),
            )
            conn.commit()
            flash("Student updated successfully!")
            return redirect(url_for("views.index"))
        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}")
        finally:
            cur.close()
            conn.close()

    cur.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cur.fetchone()
    cur.close()
    conn.close()

    return render_template("edit.html", student=student)


@views.route("/update_student/<id>", methods=["POST"])
def update_student(id):
    if request.method == "POST":
        try:
            fullname = request.form.get("fullname")
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")

            if not (fullname and username and email and password):
                flash("Missing required fields!")
                return redirect(url_for("views.index"))

            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                """
                UPDATE students
                SET fullname = %s,
                    username = %s,
                    email = %s,
                    password = %s
                WHERE id = %s
            """,
                (fullname, username, email, password, id),
            )
            conn.commit()
            cur.close()
            conn.close()
            flash("Student Updated Successfully")
            return redirect(url_for("views.index"))
        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}")


@views.route("/delete/<id>", methods=["POST", "GET"])
def delete_student(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("DELETE FROM students WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        flash("Student Removed Successfully")
        return redirect(url_for("views.index"))
    except Exception as e:
        flash(f"Error: {str(e)}")
        return redirect(url_for("views.index"))
