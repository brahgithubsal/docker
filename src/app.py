# src/app.py — Microservice API REST (Version 2.0.0 - Production Ready)
import os
import socket
import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

APP_VERSION = os.environ.get("APP_VERSION", "2.0.0")
APP_ENV = os.environ.get("APP_ENV", "production")

# Base de données en mémoire pour le lab
TASKS = [
    {'id': 1, 'task': 'Comprendre le Filesystem Linux', 'done': True},
    {'id': 2, 'task': 'Écrire un Dockerfile multi-couches', 'done': True},
    {'id': 3, 'task': 'Déployer sur un cluster Kubernetes', 'done': False},
    {'id': 4, 'task': 'Créer un pipeline CI/CD automatisé', 'done': False}
]

@app.route('/')
def home():
    return jsonify({
        'message': 'Bienvenue sur le microservice DevOps Flask !',
        'version': APP_VERSION,
        'environment': APP_ENV,
        'container_id': socket.gethostname(),
        'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat()
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'flask-task-api',
        'version': APP_VERSION,
        'tasks_count': len(TASKS)
    }), 200

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(TASKS)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json(silent=True) or {}
    if not data.get('task'):
        return jsonify({'error': 'Le champ task est requis'}), 400
    new_task = {
        'id': len(TASKS) + 1,
        'task': data['task'],
        'done': bool(data.get('done', False))
    }
    TASKS.append(new_task)
    return jsonify(new_task), 201

@app.route('/api/stats')
def get_stats():
    total = len(TASKS)
    done = sum(1 for t in TASKS if t['done'])
    return jsonify({
        'total_tasks': total,
        'completed': done,
        'pending': total - done,
        'completion_rate': f"{round((done / total) * 100, 1)}%" if total else "0%"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # 0.0.0.0 est CRITIQUE : permet d'écouter les requêtes externes au conteneur
    app.run(host='0.0.0.0', port=port)
