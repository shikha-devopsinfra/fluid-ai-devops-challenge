import os
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "appdb"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "password"),
        port=os.getenv("DB_PORT", "5432"),
        connect_timeout=3
    )


@app.route("/")
def home():
    return jsonify({
        "application": "Fluid AI DevOps Challenge",
        "version": "1.0"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/users")
def users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "database": "connected"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "database": "unavailable",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)