"""
Author: Nathan Malamud
Date: Sunday, October 20th, 2024

Goal: Define and resolve rows in excel spreadsheet
on a case by case basis.

Testing pattern matching (select Python):
   https://regex101.com/

Chat-GPT4 chat log:
  Source: https://chatgpt.com/share/671571e6-5924-8012-89c1-c888afc546ef

"""

import regex as re

# !!! WARNING: All these matching functions need to be TESTED
# This is on my TODO list - Nate
 
def match_frank_lomer(s: str) -> bool:
    pattern = r'\b(f|fra[mn]k)\s*[w]*\s*(lom[ea]r)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_vladimir_krajina(s: str) -> bool:
    pattern = r'\b(v|vlad[ia]*[mn][ei]r)\s*[j]*\s*(kraji[mn]a)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_thomas_taylor(s: str) -> bool:
    pattern = r'\b(t|tmc|t(h)?om[ai]s)\s*[mc]*\s*[mc]+\s*(ta[iy]?l[oei]?r)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_john_eastham(s: str) -> bool:
    pattern = r'\b(j|jo[ghn]?n)\s*[qwe]*\s*(e[a]?st[he]?a[mn])\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_katherine_beamish(s: str) -> bool:
    pattern = r'\b(k|[ck]atherin[e]?)\s*(i)?\s*([dbp]?e[ea]?mis[sh]*)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_gerald_straley(s: str) -> bool:
    pattern = r'\b(g|gera[ld]+)\s*[gb]+\s*(stra[y]?[il]+[e]?y)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_vernon_brink(s: str) -> bool:
    pattern = r'\b(v|vernon)\s*(c)?\s*(brink)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_john_davidson(s: str) -> bool:
    pattern = r'\b(j|john|jo[n]+)\s*(dav[iy]dson)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_adam_szczawinski(s: str) -> bool:
    pattern = r'\b(a[ef]*|adam)\s*(f)?\s*[aef]*\s*(s[zc]+[aou]*[za]+win[skiy]+)\bb'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_james_calder(s: str) -> bool:
    pattern = r'\b(j|jame[s]?)\s*(a)?\s*(cald[ei][ry])\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_freek_vrugtman(s: str) -> bool:
    pattern = r'\b(f|fr[e]+k)?\s*(v[r]+u[gt]+[a]?ma[n]+)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_william_mccalla(s: str) -> bool:
    pattern = r'\b(w[c]?|william)\s*(c|copeland)?\s*(mccal+?[la])\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_jim_pojar(s: str) -> bool:
    pattern = r'\b(j|jim|james)\s*[j]*\s*(pojar)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_roy_taylor(s: str) -> bool:
    pattern = r'\b(r|roy)\s*(l)?\s*(tayl[oe]r)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_bruce_bennett(s: str) -> bool:
    pattern = r'\b(b|b[r]?uce)\s*(a)?\s*(be[n]+e[t]+)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_beryl_zhuang(s: str) -> bool:
    pattern = r'\b(b|ber[yi]l)\s*(c)?\s*(z[h]?uang)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_trevor_goward(s: str) -> bool:
    pattern = r'\b(t|trev[eo]r)\s*(gow[ea]r[dt])\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_jeffery_saarela(s: str) -> bool:
    pattern = r'\b(j|jeff([ae]ry|r[ea]y)?)\s*(m)?\s*(saarela)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_terry_mcintosh(s: str) -> bool:
    pattern = r'\b(t|terry)\s*(t)?\s*(mcintosh)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_william_cody(s: str) -> bool:
    pattern = r'\b(w|william)\s*(j)?\s*(cody)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_fred_fodor(s: str) -> bool:
    pattern = r'\b(f|fred)\s*(fod[oi]r)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_charles_beil(s: str) -> bool:
    pattern = r'\b(c|c[h]?arles)\s*(e)?\s*(b[e]*il)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_curtis_bjork(s: str) -> bool:
    pattern = r'\b(c|k|[ck]urtis)\s*(r)?\s*(b[j]*[\S]*rk)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_jamie_fenneman(s: str) -> bool:
    pattern = r'\b(j|jamie|james)\s*(d)?\s*(fe[n]+ema[n]+)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_erin_manton(s: str) -> bool:
    pattern = r'\b(e|erin)\s*(r)?\s*(mant[oe]n)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_adolf_ceska(s: str) -> bool:
    pattern = r'\b(a|adolf)\s*[oip]*\s*(ceska)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_oluna_ceska(s: str) -> bool:
    pattern = r'\b(o|oluna)\s*(ceska)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_le_taylor(s: str) -> bool:
    pattern = r'\b(l|l[\s]+e)\s*ta[y|i]l[o]?r\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_john_pinder_moss(s: str) -> bool:
    pattern = r'\b(j|jo[hn]+)?\s*(pin[d]?er)(-)?(mo[s]+)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_wilfred_schofield(s: str) -> bool:
    pattern = r'\b(w|wi[l]?fred)\s*[b]+\s*(sc[h]?of[i]?eld)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_corinne_selby(s: str) -> bool:
    pattern = r'\b(c|corinne)\s*(j)?\s*(se[lb]+y)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_db_o_savile(s: str) -> bool:
    pattern = r'\b(d|dbo)?\s*[dbo]*\s*(sa[v]+[ei][l]+e)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_eli_wilson(s: str) -> bool:
    pattern = r'\b(a|e|[ea]li)\s*(wilson)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_linda_jennings(s: str) -> bool:
    pattern = r'\b(l|linda)\s*([p])?\s*(jenning(s)?|lips[oe]n)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_quentin_cronk(s: str) -> bool:
    pattern = r'\b(q|quentin)\s*[ceb]*\s*([ck]ro[nm][kc]?)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))
  
def match_william_randolph_taylor(s: str) -> bool:
    pattern = r'\b(wm(r)?|wi[l]+([eia]+m)?)\s*(r|randol[phf]+)?\s*(tayl[oe]r)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_fj_r_taylor(s: str) -> bool:
    pattern = r'\b(f[jr]+)\s*[jr]*\s*[jr]*\s*(tayl[oe]r)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_sandra_c_lindstrom(s: str) -> bool:
    pattern = r'\b(s|sandra)\s*[c]*\s*(lindstrom(e)?|lindstorm(e)?)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_stephen_s_talbot(s: str) -> bool:
    pattern = r'\b(s|ste[phf]+[ea]n)\s*[s]*\s*(talb[oiea]t)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))
  
def match_jc_oliveira(s: str) -> bool:
    pattern = r'\b(j|jc)\s*[c]*\s*(oliv[ei]+[r]+a?)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))
  
def match_jl_celistino(s: str) -> bool:
    pattern = r'\b(j|jl)\s*[l]+\s*(ce[li]+st[ie]*no)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_stephen_j_oliver(s: str) -> bool:
    pattern = r'\b(s|ste[phfv]+[ea]n)\s*(j)?\s*(oliv[ei]+[r]+)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))
  
def match_student(s: str) -> bool:
    pattern = r'\bstudent[s]?|graduate[s]?\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))
