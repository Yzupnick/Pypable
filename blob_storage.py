from base_destination import BaseDestination
import azure

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
