import os
import glob

ROOT = '/Library/WebServer/Documents/press_releases/'

thumb  = glob.glob(ROOT + 'thumbnails/PIA*/PIA*_thumb.*')
small  = glob.glob(ROOT + 'small/PIA*/PIA*_small.*')
medium = glob.glob(ROOT + 'medium/PIA*/PIA*_med.*')
pages  = glob.glob(ROOT + 'pages/PIA*/PIA*.html')

thumb  = {x.rpartition('xxx/')[2][:8]:x for x in thumb}
small  = {x.rpartition('xxx/')[2][:8]:x for x in small}
medium = {x.rpartition('xxx/')[2][:8]:x for x in medium}
pages  = {x.rpartition('xxx/')[2][:8]:x for x in pages}

thumb_wo_page  = set(thumb) - set(pages)
small_wo_page  = set(small) - set(pages)
medium_wo_page = set(medium) - set(pages)

page_wo_thumb  = set(pages) - set(thumb)
page_wo_small  = set(pages) - set(small)
page_wo_medium = set(pages) - set(medium)

print('#', len(page_wo_thumb), len(page_wo_small), len(page_wo_medium))
# 0 0 0

print('#', len(thumb_wo_page), len(small_wo_page), len(medium_wo_page))
# 2293 2412 2415

# Careful!!
for key in thumb_wo_page:
    print(thumb[key])
    os.remove(thumb[key])

for key in small_wo_page:
    print(small[key])
    os.remove(small[key])

for key in medium_wo_page:
    print(medium[key])
    os.remove(medium[key])


