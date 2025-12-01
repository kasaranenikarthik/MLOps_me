import os
import json
import redis
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text

app = Flask(__name__)

# Database connection
engine = create_engine(os.environ['DATABASE_URL'])

# Redis connection
cache = redis.from_url(os.environ['REDIS_URL'])

@app.route('/health')
def health():
    """Health check endpoint for Docker"""
    try:
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        cache.ping()
        return jsonify({'status': 'healthy', 'db': 'ok', 'cache': 'ok'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Try cache first
    cached = cache.get('tasks:all')
    if cached:
        tasks = json.loads(cached.decode()) 
        return jsonify({'source': 'cache', 'tasks': tasks})
    
    with engine.connect() as conn:
        result = conn.execute(text('SELECT * FROM tasks'))
        tasks = [dict(row._mapping) for row in result]
    
    # Cache for 6 seconds
    cache.setex('tasks:all', 6, json.dumps(tasks, default=str))
    return jsonify({'source': 'database', 'tasks': tasks})

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    with engine.connect() as conn:
        existing = conn.execute(
            text('SELECT 1 FROM tasks WHERE title = :title'),
            {'title': data['title']}
        ).fetchone()

        if existing:
            return jsonify({'error': 'Task already exists'}), 409
        
        conn.execute(
            text('INSERT INTO tasks (title, status) VALUES (:title, :status)'),
            {'title': data['title'], 'status': 'pending'}
        )
        conn.commit()
    
    # Invalidate cache
    cache.delete('tasks:all')
    
    # Queue background job
    cache.lpush('task:queue', data['title'])
    
    return jsonify({'message': 'Task created'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)