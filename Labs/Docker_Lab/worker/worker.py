import os
import time
import redis
import psycopg2

redis_client = redis.from_url(os.environ['REDIS_URL'])

def get_db_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'])

def process_task(task_name):
    """Simulate processing a task"""
    print(f"Processing task: {task_name}")
    time.sleep(2)  # Simulate work
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET status = 'processing' WHERE title = %s",
        (task_name,)
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Completed task: {task_name}")

def complete_task(task_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET status = 'completed' WHERE title = %s",
        (task_name,)
    )
    conn.commit()
    cur.close()
    conn.close()

def main():
    print("Worker started, waiting for tasks...")
    while True:
        # Blocking pop from queue
        task = redis_client.brpop('task:queue', timeout=5)
        if task:
            task_name = task[1].decode()
            print(f"Received task: {task_name}")
            process_task(task_name)
            time.sleep(10)  # Simulate some delay before marking complete
            complete_task(task_name)
            print(f"Task marked as completed: {task_name}")

if __name__ == '__main__':
    main()