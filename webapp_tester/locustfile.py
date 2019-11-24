from locust import HttpLocust, TaskSequence, task, seq_task
import os
import uuid
import random

def between(min_wait, max_wait):
    return lambda instance: min_wait + random.random() * (max_wait - min_wait)

class FEBehaviour(TaskSequence):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.object_pool = []

    @seq_task(3)
    @task(2)
    def get_all(self):
        self.client.get("/")

    @seq_task(2)
    @task(8)
    def get_one(self):
        if len(self.object_pool) > 0:
            id = random.choice(self.object_pool)
            self.client.get("/objs/" + id)

    @seq_task(1)
    @task(8)
    def put_one(self):
        id = str(uuid.uuid4())
        response = self.client.put("/objs/" + id, os.urandom(random.randrange(512, 1024 * 4096)))
        if response.ok:
            self.object_pool.append(id)

    @seq_task(4)
    @task(6)
    def delete_one(self):
        if len(self.object_pool) > 0:
            id = self.object_pool.pop()
            self.client.delete("/objs/" + id)

    #@seq_task(5)
    #@task(1)
    def delete_all(self):
        self.client.delete("/")


class TestBed(HttpLocust):
    task_set = FEBehaviour
    wait_time = between(0.5, 1.5)
    host = "http://10.0.3.191:8000"

