from django import template
register = template.Library()

# grep, because, why not?!
import re
@register.filter
def grep(*args, **kwargs):
    # Due to the million of options that exist in grep...
    # This toy example only supports the most useful/convienent to implement flags
    options = {
        'V': '-',   'version': '-',         # print GREP version; just check if given
        'e': '-',   'regexp': '-',          # update patterns with whatever is next
        'f': '-',   'file': '-',            # obtain patterns from file by reading line by line
        'i': '-',    'ignore-case': '-',    # match on patterns while using str.lower() on all involved strings; just check if given
        'v': '-',    'invert-match': '-',   # return all string that don't match; just check if supplied
        'x': '-',    'line-regexp': '-',    # only return 100% matches of patterns; just check if supplied
    }
    options.update(kwargs)
    # check for -V or --version
    if options['V'] != '-' or options['version'] != '-':
        return 'grep (DJANGO grep) 3.7'
    # # Case by case assignment for pattern
    # if -e or --regexp is passed
    if options['e'] != '-' and options['regexp'] != '-':
        pattern = re.compile(args[0])
    # if -i or --ignore-case is passed
    elif options['i'] != '-' and options['ignore-case'] != '-':
        pattern = re.compile(str(args[0]).lower())
    # if -x or line-regexp is passed
    elif options['x'] != '-' and options['line-regexp'] != '-':
        pattern = r'^{}$'.format(args[0])
    # base case
    else: re.compile(args[0])

    # # Case by case assignment/behaviour for data
    # if the -f or --file option is passed
    if options['f'] != '-' or options['file'] != '-':
        data = [ line.strip() for line in open(args[1], 'r').readlines() ]
    # if -i or --ignore-case is passed
    elif options['i'] != '-' or options['ignore-case'] != '-':
        data = list(str(args[1]).lower())
    # base case
    else: data = list(args[1])

    # find matches to the regex
    matches = [ re.search(pattern, data[0]) if len(data) == 1 else re.findall(pattern, sample) for sample in data ]

    return [ item for item in data if item not in matches ] if options['v'] != '-' or options['invert-match'] != '-' else matches

# Expose grep as a viable filter to use
register.filter('grep', grep)

## # # # # # # # # # # # # # # ##
#      END OF TOY EXAMPLES      #
## # # # # # # # # # # # # # # ##
## BEGIN REAL TEMPLATE FILTERS ##