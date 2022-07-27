from kivy.storage.jsonstore import JsonStore


class _Storage(JsonStore):
    def __init__(self, save_filename):
        super().__init__(save_filename)

    def add_data(self, key, **content):
        self.put(key, **content)

    def get_data(self, key):
        return self.get(key)

    def is_exist_data(self, key):
        return self.exists(key)

    def delete_data(self, key):
        self.delete(key)


Storage = _Storage("prj_openStoys.json")
