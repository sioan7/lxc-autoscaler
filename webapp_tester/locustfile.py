from locust import HttpLocust, TaskSet
import uuid
import random

object_pool = []

def get_all(l):
    l.client.get("/")

def delete_all(l):
    l.client.delete("/")

def get_one(l):
    id = object_pool[random.randrange(len(object_pool) - 1)]
    l.client.get("/objs/" + id)

def put_one(l):
    id = str(uuid.uuid4())
    object_pool.append(id)
    l.client.put("/objs/" + id, "object with id " + id)

def delete_one(l):
    id = object_pool.pop()
    l.client.delete("/objs/" + id)

class UserBehavior(TaskSet):
    tasks = {
        get_all: 10,
        put_one: 10,
        get_one: 20,
        delete_one: 9,
    }

    def on_stop(self):
        delete_all(self)

class TestBed(HttpLocust):
    task_set = UserBehavior
    min_wait = 500
    max_wait = 1500
    host = "http://10.0.3.191:8000"

