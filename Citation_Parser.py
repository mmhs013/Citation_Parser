# import urllib.request
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Google Scholar Profile Parsing
gs_profile_link = 'https://scholar.google.com/citations?user=ub2WBpoAAAAJ'

page = requests.get(gs_profile_link).text
soup = BeautifulSoup(page)

total_cite = int(soup.findAll('td',{'class':'gsc_rsb_std'})[0].text)

div = soup.findAll('tr',{'class':'gsc_a_tr'})

for i in range(len(div)):
    DicData = {
        'Name' : div[i].findAll('a',{'class':'gsc_a_at'})[0].text,
        'Authors' : div[i].findAll('div',{'class':'gs_gray'})[0].text,
        'Publisher' : div[i].findAll('div',{'class':'gs_gray'})[1].text[:-6],
        'Year' : div[i].findAll('td',{'class':'gsc_a_y'})[0].text,
        'Citation' : div[i].findAll('td',{'class':'gsc_a_c'})[0].text,
    }
    
    if i == 0:
        gs_profile_papers = pd.DataFrame(DicData, index=[i])
    
    else:
        gs_profile_papers = gs_profile_papers.append(DicData,ignore_index=True)      

gs_pymk_cite = int(gs_profile_papers[gs_profile_papers.Name == 'pyMannKendall: a python package for non parametric Mann Kendall family of trend tests.'].Citation.iloc[0])



# Researchgate pyMannKendall paper citetion parsing
rg_profile_link = 'https://www.researchgate.net/publication/334688255_pyMannKendall_a_python_package_for_non_parametric_Mann_Kendall_family_of_trend_tests/citations'

page = requests.get(rg_profile_link).text
soup = BeautifulSoup(page)

rg_pymk_cite = soup.findAll('div',{'class':'nova-e-text nova-e-text--size-m nova-e-text--family-sans-serif nova-e-text--spacing-none nova-e-text--color-inherit nova-c-nav__item-label'})[0].text
rg_pymk_cite = int(rg_pymk_cite.replace('Citations (','').replace(')',''))


# Badge create via shields.io
badge_link = {
    'gs_pymk_cite' : "https://img.shields.io/badge/Citations-{cite}-_.svg?logo=google-scholar&labelColor=f0f0f0&color=4499ff".format(cite = gs_pymk_cite),
    'rg_pymk_cite' : "https://img.shields.io/badge/Citations-{cite}-_.svg?logo=researchgate&labelColor=4f4f4f&color=00ddaa".format(cite = rg_pymk_cite),
}

for itm in badge_link.items():
    with open('images/'+itm[0] + '.svg', 'wb') as f:
        f.write(requests.get(itm[1]).content)