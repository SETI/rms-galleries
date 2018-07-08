################################################################################
# Program to regenerate all the PIA pages
################################################################################

from piapage import PiaPage

for pia in range(1,23000):
    if pia%100 == 0: print pia

    try:
        p = PiaPage(pia)
    except IOError:
        print pia, 'IOError'
        continue
    except ValueError as e:
        print pia, e
        continue

    if not p.is_planetary:
        print pia, 'Not planetary'
        continue

    if not p.is_planetary: continue

    path = '/Users/mark/GitHub/pds-website/website' + p.local_html_url

    p.write_jekyll(path)

################################################################################
