import piapage
import pickle

info = {}
for pia in range(1, 23000):
    if pia % 100 == 0: print pia

    try:
        p = piapage.PiaPage(pia)
    except IOError:
        print pia, 'IOError'
        continue
    except ValueError as e:
        print pia, e
        continue

    if not p.is_planetary:
        print pia, 'Not planetary'
        continue

    keywords_used = set()
    keywords_used |= set(p.missions)
    keywords_used |= set(p.hosts)
    keywords_used |= set(p.host_types)
    keywords_used |= set(p.instruments)
    keywords_used |= set(p.detectors)
    keywords_used |= set(p.targets)
    keywords_used |= set(p.target_types)
    keywords_used |= set(p.systems)
    extra_keywords = set(p.keywords) - keywords_used
    extra_keywords = list(extra_keywords)
    extra_keywords.sort()

    info[p.id] = (p.release_date, p.title,
                  p.is_movie, p.is_color, p.is_grayscale,
                  p.missions, p.hosts, p.host_types, p.instruments, p.detectors,
                  p.targets, p.target_types, p.systems, extra_keywords,
                  p.dates,
                  p.local_html_url, p.local_thumbnail_url,
                  p.local_small_url, p.local_medium_url)

f = open('piapage_catalog.pickle', 'w')
pickle.dump(info, f)
f.close()

