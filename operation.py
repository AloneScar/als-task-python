import snowflake.client
import psycopg2
import time
import json

def get_snowflake_uuid() -> int:
    return snowflake.client.get_guid()

# def save_tasks_json(tasks_obj, path):
#     with open(mode="w", file=path) as f:
#         json.dump(fp=f, obj=tasks_obj, default=lambda obj: obj.__dict__, sort_keys=True, indent=2)

# def load_tasks_json(path) -> dict:
#     with open(mode="r", file=path) as f:
#         return json.load(fp=f)

def load_tasks(cur) -> list:
    cur.execute('select task from tasks')
    return list(map(lambda task: task[0], cur.fetchall()))

def create_tasks_table(conn, cur):
    cur.execute('''
        CREATE TABLE tasks (
            id serial PRIMARY KEY,
            task json NOT NULL
        );
    ''')
    conn.commit()

def connect_database():
    conn = psycopg2.connect(dbname='als_task', user='postgres', password='als', host='127.0.0.1', port='5432')
    cur = conn.cursor()
    return (conn, cur)

def drop_table(conn, cur):
    cur.execute('drop table if exists tasks')
    conn.commit()


def default_task(
        content,
        depth = 0,
        comments = None,
        state = "Todo",
        dead_time = None,
        prev_task = None,
        next_task = None
    ):
    return {
        "task_id": get_snowflake_uuid(),
        "depth": depth,
        "content": content,
        "comments": comments,
        "state": "Todo",
        "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        "update_time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        "dead_time": dead_time,
        "prev_task": prev_task,
        "next_task": next_task
    }

def add_task(conn, cur, task) -> bool:
    cur.execute("insert into tasks (task) values ('%s')" % json.dumps(task))
    conn.commit()


if __name__ == '__main__':
    conn, cur = connect_database()

    drop_table(conn, cur)
    create_tasks_table(conn, cur)

    add_task(conn, cur, default_task("fasdfds"))
    add_task(conn, cur, default_task("fasdfds"))
    add_task(conn, cur, default_task("fasdfds"))
    add_task(conn, cur, default_task("fasdfds"))

    tasks = load_tasks(cur)
    print(tasks)