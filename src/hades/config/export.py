import logging
import re
import collections

import netaddr

from hades.config.loader import get_config


logger = logging.getLogger('hades.config.export')
shell_types = (int, str, bool, netaddr.IPAddress, netaddr.IPNetwork)
pattern = re.compile(r'([^a-zA-Z0-9_])')
replacement = r'\\\1'


def escape(value):
    """
    Escape a string for shell argument use.
    shlex.quote breaks unfortunately on certain strings
    """
    return pattern.sub(replacement, str(value))


def main():
    config = get_config()
    for name, value in config.items():
        escaped_name = escape(str(name))
        if isinstance(value, shell_types):
            print("export {}={}".format(escaped_name, escape(value)))
        elif isinstance(value, collections.Mapping):
            print("declare -A {}".format(name))
            for k, v in value.items():
                if isinstance(v, shell_types):
                    print("{}[{}]={}".format(escaped_name, escape(str(k)),
                                             escape(str(v))))
            print("export {}".format(escaped_name))
        elif isinstance(value, collections.Sequence):
            print("declare -a {}".format(name))
            for index, v in enumerate(value):
                if isinstance(v, shell_types):
                    print("{}[{}]={}".format(escaped_name, index,
                                             escape(str(v))))
            print("export {}".format(escaped_name))


if __name__ == '__main__':
    main()
