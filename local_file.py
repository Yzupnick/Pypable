import os
import azure

class BaseDestination(object):
    def __init__(self,parser):
        argument = "--{}".format(self.name)
        parser.add_argument(argument,
                            dest='send',
                            action="store_const",
                            const=self,
                            help=self.help_text)


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


class AzureBlobStorage(BaseDestination):
    name = "blobs"
    help_text = "save to azure blob storage"

    def __init__(self,parser):
        parser.add_argument('--acount', dest='acount')
        parser.add_argument('--key', dest='key')
        parser.add_argument('--container', dest='container')
        super().__init__(parser)

    def __call__(self,args, contents):
        self.blob_service = azure.storage.BlobService(account_name=args.account, account_key=args.key)
        if args.files:
            self._copy_files(args, contents)
        else:
            self._send_string(args, contents)

    def _copy_files(self,args, file_names):
        for file_name in [fn.strip() for fn in file_names.split('\n')]:
            self.blob_service.put_block_blob_from_path(
                args.container,
                file_name,
                file_name
            )

    def _send_string(self,args, contants):
        self.blob_service.put_block_blob_from_text(
            args.container,
            args.name,
            contents
        )
