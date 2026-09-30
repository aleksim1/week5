import os
import requests
import pymysql
import pymysql.cursors

from datetime import datetime, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)

REST_API_KEY = os.getenv("REST_COUNTRIES_API_KEY")


def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "changeme"),
        database=os.getenv("DB_NAME", "appdb"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )

def init_db():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS page_visits (
                    id INT PRIMARY KEY,
                    visits INT DEFAULT 0
                )
            """)
            cursor.execute("""
                INSERT IGNORE INTO page_visits (id, visits) VALUES (1, 0)
            """)
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Database initialization warning: {e}")

init_db()

@app.route("/api/visit", methods=["POST"])
def visit():
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE page_visits SET visits = visits + 1 WHERE id = 1"
            )

            cursor.execute(
                "SELECT visits FROM page_visits WHERE id = 1"
            )

            row = cursor.fetchone()

            if not row:
                return jsonify({"error": "Page visits not found"}), 404

            return jsonify({"visits": row["visits"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()


@app.route("/api/time", methods=["GET"])
def get_time():
    return jsonify({
        "serverTime": datetime.now(timezone.utc).isoformat()
    })

@app.route("/api/capital")
def get_capital():
    country = request.args.get("country")
    if not country:
        return jsonify({"error": "Country parameter missing"}), 400

    url = "https://api.restcountries.com/countries/v5/names.common/" + requests.utils.quote(country)
    headers = {"Authorization": f"Bearer {REST_API_KEY}"}

    try:
        response = requests.get(
            url,
            headers=headers,
            params={"response_fields": "names.common,capitals"},
            timeout=10,
        )

        if response.status_code == 404:
            return jsonify({"error": "Country not found"}), 404
        response.raise_for_status()

        objects = response.json().get("data", {}).get("objects", [])
        if not objects:
            return jsonify({"error": "Country not found"}), 404

        capitals = objects[0].get("capitals") or []
        capital = capitals[0]["name"] if capitals else "Unknown"
        return jsonify({"capital": capital})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 502

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
