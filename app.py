import os
import random
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)
author_name = os.environ.get("AUTHOR_NAME", "Tolgahan")

cool_facts = [
    "Docker was released in 2013.",
    "Containers are not VMs, they share the OS kernel instead of virtualizing hardware.",
    "Python is named after Monty Python, not the snake! (I didn't know this)",
    "The first computer bug was an actual real bug (a moth)."
]

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_PORT = os.environ.get("DB_PORT", "5432")

def get_db_connection():
    """Establishes connection to PostgreSQL"""
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    conn.autocommit = True
    return conn

def init_db():
    """Initializes the database table for tracking state"""
    if DB_HOST:
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS api_stats (id INTEGER PRIMARY KEY, fact_requests INTEGER)")
                cur.execute("INSERT INTO api_stats (id, fact_requests) VALUES (1, 0) ON CONFLICT (id) DO NOTHING")
            conn.close()
            print("Connected to PostgreSQL and initialized table.")
        except Exception as e:
            print(f"Database initialization error: {e}")

init_db()

@app.route('/health')
def health_check():
    return jsonify({"status": "ok", "message": "App is running smoothly."})

@app.route('/fact')
def get_random_fact():
    if DB_HOST:
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("UPDATE api_stats SET fact_requests = fact_requests + 1 WHERE id = 1")
            conn.close()
        except Exception as e:
            print(f"DB Error: {e}")

    selected_fact = random.choice(cool_facts)
    return jsonify({
        "provided_by": author_name,
        "fact": selected_fact
    })

@app.route('/greet')
def greet_user():
    user_name = request.args.get("name", "Guest")
    return jsonify({
        "message": f"Hello {user_name}! Welcome to {author_name}'s API."
    })

@app.route('/stats')
def get_stats():
    total_requests = 0
    storage = "memory (no DB)"
    
    if DB_HOST:
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT fact_requests FROM api_stats WHERE id = 1")
                result = cur.fetchone()
                if result:
                    total_requests = result[0]
                    storage = "postgresql"
            conn.close()
        except Exception as e:
            print(f"DB Error: {e}")

    return jsonify({
        "author": author_name,
        "total_facts_available": len(cool_facts),
        "total_facts_served": total_requests,
        "state_storage": storage
    })

if __name__ == "__main__":
    app_port = int(os.environ.get("PORT", 8080))
    print(f"Starting the Fact API on port {app_port}...")
    app.run(host="0.0.0.0", port=app_port)