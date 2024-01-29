class RelativePathFilter(logging.Filter):
    def filter(self, record):
        record.relativePath = os.path.relpath(record.pathname)
        return True

def apply_advanced_log_tracking():
    """Apply filter to all existing loggers, this way we can produce clickable logs for pyCharm"""
    for logger in logging.Logger.manager.loggerDict.values():
        if isinstance(logger, logging.Logger):
            logger.addFilter(RelativePathFilter())

    # Apply filter to all new loggers
    original_get_logger = logging.getLogger
    logging.getLogger = lambda *args, **kwargs: (x := original_get_logger(*args, **kwargs)).addFilter(
        RelativePathFilter()) or x

    # Apply filter to root logger
    logging.root.addFilter(RelativePathFilter())

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(relativePath)s:%(lineno)d %(asctime)s {%(name)s} [%(levelname)s] %(message)s',
    )


def print_tree(directory, prefix=''):
    files = []
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"{directory} is not a directory")

    # List all files and directories in the current directory
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            # It's a directory, print and recurse into it
            print(prefix + '├── ' + item)
            print_tree(path, prefix + '│   ')
        else:
            # It's a file, add to the list of files
            files.append(item)

    # Print the list of files
    for file in files:
        print(prefix + '├── ' + file)
