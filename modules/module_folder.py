from abc import abstractmethod
from pynecone import ModuleProvider, ProtoShell, ProtoCmd, Config


class FolderProvider(ModuleProvider):

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_path(self):
        pass

    @abstractmethod
    def is_folder(self):
        pass

    @abstractmethod
    def get_children(self):
        pass

    @abstractmethod
    def get_stat(self):
        pass

    @abstractmethod
    def get_hash(self):
        pass

    @abstractmethod
    def create_folder(self, name):
        pass

    @abstractmethod
    def create_file(self, name, data):
        pass

    @abstractmethod
    def delete(self, name):
        pass


class Folder(ProtoShell):

    class Copy(ProtoCmd):

        def __init__(self):
            super().__init__('copy',
                             'copy from source_path to target_path')

        def add_arguments(self, parser):
            parser.add_argument('source_path', help="specifies the source_path")
            parser.add_argument('target_path', help="specifies the target_path")

        def run(self, args):
            Folder.from_path(args.source_path).copy(Folder.from_path(args.target_path))

    class Get(ProtoCmd):

        def __init__(self):
            super().__init__('get',
                             'download folder or file from path')

        def add_arguments(self, parser):
            parser.add_argument('path', help="specifies the path")
            parser.add_argument('--local_path', help="specifies the local path where to save", default='.')

        def run(self, args):
            Folder.from_path(args.path).get(args.local_path)

    class Put(ProtoCmd):

        def __init__(self):
            super().__init__('put',
                             'upload folder or file to path')

        def add_arguments(self, parser):
            parser.add_argument('local_path', help="specifies the local path to upload")
            parser.add_argument('target_path', help="specifies the target path")

        def run(self, args):
            Folder.from_path(args.target_path).put(args.local_path)

    class Delete(ProtoCmd):

        def __init__(self):
            super().__init__('delete',
                             'delete path')

        def add_arguments(self, parser):
            parser.add_argument('path', help="specifies the path to be deleted")

        def run(self, args):
            Folder.from_path(args.path).delete()

    class List(ProtoCmd):

        def __init__(self):
            super().__init__('list',
                             'list files and folders on path')

        def add_arguments(self, parser):
            parser.add_argument('path', help="specifies the path to be listed", default=None, const=None, nargs='?')

        def run(self, args):
            if args.path:
                if args.path:

                    folder = Folder.from_path(args.path)
                    for c in folder.get_children():
                        print(c.get_name())
                else:
                    for mount in Config.init().list_mount():
                        print(mount['name'])
            else:
                for mount in Config.init().list_mount():
                    print(mount['name'])

    class Checksum(ProtoCmd):

        def __init__(self):
            super().__init__('checksum',
                             'calculate the checksum of the folder at path')

        def add_arguments(self, parser):
            parser.add_argument('path', help="specifies the path to be deleted")

        def run(self, args):
            print(Folder.from_path(args.path).hash())

    def __init__(self):
        super().__init__('folder', [Folder.Copy(), Folder.Get(), Folder.Put(), Folder.Delete(), Folder.List(), Folder.Checksum()], 'folder shell')

    @classmethod
    def from_path(cls, path):
        config = Config.init()
        mount_path = '/{0}'.format(path.split('/')[1])
        folder_path = '/'.join(path.split('/')[2:])
        mount = config.get_entry_instance('mounts', mount_path)
        return mount.get_folder(folder_path)


class Module(ModuleProvider):

    def get_instance(self, **kwargs):
        return Folder()