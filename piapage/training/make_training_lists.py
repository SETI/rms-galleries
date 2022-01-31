import numpy as np
import pickle
import piapage
from gallerypage import GalleryPage

from piapage.MAX_PIAPAGE import MAX_PIAPAGE

# Create dictionaries keyed by paragraph strings, which return the number of
# occurrences of the given string

captions = {}
backgrounds = {}

for pia in range(1, MAX_PIAPAGE):
    if pia % 100 == 0: print pia

    try:
        p = piapage.PiaPage(pia)
    except (IOError, ValueError):
        pass

    if not p.is_planetary: continue

    soup = p.caption_soup
    for para_soup in soup.find_all('p'):
        text = GalleryPage.soup_as_text(para_soup)

        if text in captions:
            captions[text] += 1
        else:
            captions[text] = 1

    soup = p.background_soup
    for para_soup in soup.find_all('p'):
        text = GalleryPage.soup_as_text(para_soup)

        if text in backgrounds:
            backgrounds[text] += 1
        else:
            backgrounds[text] = 1

# Create lists of tuples (count, text)
background_list = [(v,k) for (k,v) in backgrounds.iteritems()]
caption_list = [(v,k) for (k,v) in captions.iteritems()]

background_list.sort()
caption_list.sort()

# Insert interactive testing here
print len([c for c in caption_list if c[0] == 1]),
print len([c for c in caption_list if c[0] > 1])
print len([b for b in background_list if b[0] == 1]),
print len([b for b in background_list if b[0] > 1])

# # 46273 2381
# # 621 834
# 
# 50202 2645
# 678 894

# [c for c in caption_list if c[0] > 1]
# [b for b in background_list if b[0] <= 1]

background_text = [b[1] for b in background_list]
caption_text = [c[1] for c in caption_list]

np.random.shuffle(background_text)
np.random.shuffle(caption_text)

f = open('backgrounds.pickle', 'w')
pickle.dump(background_list, f)
f.close()

f = open('captions.pickle', 'w')
pickle.dump(caption_list[:5000], f)
f.close()
