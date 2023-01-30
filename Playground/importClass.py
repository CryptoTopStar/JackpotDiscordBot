class API:
    def __init__(self):
        self.x = 0
        self.dict = {}

_instance = None
def get_instance():
    global _instance
    if _instance is None:
        _instance = API()
    return _instance

def add(_instance, x, y):
    _instance.dict[x] = y
    return _instance.dict