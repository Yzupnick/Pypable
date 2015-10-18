class BaseDestination(object):
    def __init__(self,parser):
        argument = "--{}".format(self.name)
        parser.add_argument(argument,
                            dest='send',
                            action="store_const",
                            const=self,
                            help=self.help_text)


