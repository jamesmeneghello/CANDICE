from candice_types import StorageBase

class UrlStorage(StorageBase):
    def store(self, data):
        if data:
            print('Storing data to %s...' % self.get_path())
            distutils.dir_util.copy_tree(data, self.get_path())
    
    def flush(self):
        if self.exists():
            print('Removing data from %s...' % self.get_path())
            distutils.dir_util.remove_tree(self.get_path())

    def get_path(self):
        return os.path.join(self.storage_path, 'data', self.request.url.with_www().replace('http://',''))

    def get_base_path(self):
        return os.path.join(self.storage_path, 'data')

    def exists(self):
        return os.path.isdir(self.get_path())

storage_types = {
    'UrlStorage': UrlStorage
}