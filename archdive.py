#!/usr/bin/python3
" dive into music archive and perform maintenance or analyis or report tasks on all files"
import sys, os, re
from phileas import _html40 as h
class shared:
    pass

def vprint(this_verbosity, *pp, **kw):
    if shared.verbosity >= this_verbosity:
        return print(*pp, **kw)


def process_child(child_name):
    vprint(2, "applying command '%s' to child directory '%s'"
          %(shared.command, child_name))
    for title in os.listdir(child_name):
        vprint(1, "applying command '%s' to subdir name (= music title) '%s'"
               % (shared.command, title))
        # ...


def main():
    # using same coding technique as music mailer for as long as this seems wise!)
    script_filename = sys.argv.pop(0)
    script_shortname = os.path.split(script_filename)[1]
    ok_commands = ('check', 'improve', 'list', 'quit')
    shared.command = (sys.argv and sys.argv.pop(0)) or 'check'
    shared.verbosity = sum([a in ('-v', '--verbose') for a in sys.argv])
    if shared.command not in ok_commands:
        print("error: %s is not one of %s." %(shared.command, ok_commands))
        sys.exit(999)
    cwd = os.getcwd()
    if not cwd.endswith('Archive'):
        print("error: %s doesn't look like an Archive directory." % (cwd))
        sys.exit(998)
    child_name_list = (
        (sys.argv and not sys.argv[0].startswith('-')) and sys.argv.pop(0)
        or sorted(os.listdir())
    )
    for child_name in child_name_list:
        if not os.path.isdir(child_name):
            vprint (2, "ignoring plain file at top level of archive '%s'" % child_name)
            continue
        elif len(child_name)==1 and 'A' <= child_name <= 'Z':
            process_child(child_name)
        else:
            vprint(2, "ignoring directory %s at top level of archive (name is not a capital letter)"
                   % child_name)
            continue
if __name__ == '__main__':
    main()
