import piapage
import numpy as np
import pickle

paragraphs = {}
for pia in range(1, 23000):
    if pia % 100 == 0: print pia

    try:
        p = piapage.PiaPage(pia)
    except IOError:
        pass

    if not p.is_planetary: continue

    soup = p.caption_soup
    for para_soup in soup.find_all('p'):
        text = para_soup.text
        text = str(''.join([c if ord(c) < 128 else ' ' for c in text]))
        text = text.strip()
        if text in paragraphs:
            paragraphs[text] += 1
        else:
            paragraphs[text] = 1

    captions = [key for key in paragraphs if paragraphs[key] == 1]
    np.random.shuffle(captions)




import piapage
import numpy as np

paragraphs = {}
for pia in range(1, 23000):
    if pia % 100 == 0: print pia

    try:
        p = piapage.PiaPage(pia)
    except IOError:
        pass

    if not p.is_planetary: continue

    soup = p.background_soup
    for para_soup in soup.find_all('p'):
        text = para_soup.text
        text = str(''.join([c if ord(c) < 128 else ' ' for c in text]))
        text = text.strip()
        if text in paragraphs:
            paragraphs[text] += 1
        else:
            paragraphs[text] = 1

    backgrounds = [key for key in paragraphs if paragraphs[key] >= 2]
    np.random.shuffle(backgrounds)

    test_backgrounds = [key for key in paragraphs if paragraphs[key] == 1]
    np.random.shuffle(test_backgrounds)


info = {}
for pia in range(1, 23000):
    if pia % 100 == 0: print pia

    try:
        p = piapage.PiaPage(pia)
    except IOError:
        pass

    if not p.is_planetary: continue

    keywords_used = set()
    keywords_used |= set(p.missions)
    keywords_used |= set(p.hosts)
    keywords_used |= set(p.instruments)
    keywords_used |= set(p.targets)
    keywords_used |= set(p.target_types)
    keywords_used |= set(p.planets)
    extra_keywords = set(p.keywords) - keywords_used
    extra_keywords = list(extra_keywords)
    extra_keywords.sort()

    info[p.id] = (p.release_date, p.title, p.missions, p.hosts, p.instruments,
                  p.targets, p.target_types, p.planets, extra_keywords,
                  p.dates)
