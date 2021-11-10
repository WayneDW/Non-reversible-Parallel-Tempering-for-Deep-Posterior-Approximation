import sys

filename = sys.argv[1]


with open(filename + '_v2', 'w') as the_file:
    for l in open(filename):
        l = l.strip()
        if l.startswith('Epoch') or l.startswith('Heating') or l.startswith('Initial') or l.startswith('Cooling') or l.startswith('Generate') or l.startswith('SWAG') or l.startswith('Using') or l.startswith('Files') or l.startswith('Namespace'):
            the_file.write(l + '\n')
