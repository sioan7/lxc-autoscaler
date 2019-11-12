from locust import HttpLocust, TaskSet

def get_all(l):
    l.client.get("/")

def delete_all(l):
    l.client.delete("/")

def get_one(l, id):
    l.client.get("/objs/" + id)

def put_one(l, id):
    l.client.put("/objs/" + id, "object with id " + id)

def delete_one(l, id):
    l.client.delete("/objs/" + id)

class UserBehavior(TaskSet):
    tasks = {index: 2, profile: 1}

    def on_start(self):
        get_all(self)

    def on_stop(self):
        delete_all(self)

class TestBed(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
