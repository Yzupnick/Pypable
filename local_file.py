import os
from base_destination import BaseDestination

class LocalFile(BaseDestination):
    name = "local"
    help_text = "save the file to a local location"

    def __init__(self,parser):
        parser.add_argument('--copy_location',
                            dest='copy_location')
        super().__init__(parser)

    def __call__(self,args, contents):
        if args.files:
            self._copy_files(args, contents)
        else:
            self._save_string_as_file(args, contents)

    def _copy_files(self,args, file_names):
        copy_location = args.copy_location
        for file_name in [fn.strip() for fn in file_names.split('\n')]:
            with open(file_name,'r') as source:
                new_name = os.path.join(copy_location,file_name)
                with open(new_name,'w') as dest:
                    dest.write(source.read())


    def _save_string_as_file(self,args, contants):
        with open(args.name, 'w') as new_file:
            new_file.write(contants)


