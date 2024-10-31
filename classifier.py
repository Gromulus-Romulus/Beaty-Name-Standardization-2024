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
    pattern = r'\b(frank)\s*(lomer)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_vladimir_krajina(s: str) -> bool:
    pattern = r'\b(vladimir)\s*(j\.?\s*)?(krajina)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_thomas_taylor(s: str) -> bool:
    pattern = r'\b(thomas)\s*(m\.?c\.?)?\s*(taylor)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_john_eastham(s: str) -> bool:
    pattern = r'\b(john)\s*(w\.?)?\s*(eastham)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_katherine_beamish(s: str) -> bool:
    pattern = r'\b(katherine)\s*(i\.?)?\s*(beamish)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_gerald_straley(s: str) -> bool:
    pattern = r'\b(gerald)\s*(b\.?)?\s*(straley)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_vernon_brink(s: str) -> bool:
    pattern = r'\b(vernon)\s*(c\.?)?\s*(brink)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_john_davidson(s: str) -> bool:
    pattern = r'\b(john)\s*(davidson)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_adam_szczawinski(s: str) -> bool:
    pattern = r'\b(adam)\s*(f\.?)?\s*(szczawinski)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_james_calder(s: str) -> bool:
    pattern = r'\b(james)\s*(a\.?)?\s*(calder)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_freek_vrugtman(s: str) -> bool:
    pattern = r'\b(freek)\s*(vrugtman)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_william_mccalla(s: str) -> bool:
    pattern = r'\b(william)\s*(copeland)?\s*(mccalla)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_jim_pojar(s: str) -> bool:
    pattern = r'\b(j)?(j+\.?|jim|james)\s*(j?\.?)\s*pojar\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_roy_taylor(s: str) -> bool:
    pattern = r'\b(roy)\s*(l\.?)?\s*(taylor)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_bruce_bennett(s: str) -> bool:
    pattern = r'\b(bruce)\s*(a\.?)?\s*(bennett)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_beryl_zhuang(s: str) -> bool:
    pattern = r'\b(beryl)\s*(c\.?)?\s*(zhuang)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_trevor_goward(s: str) -> bool:
    pattern = r'\b(trevor)\s*(goward)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_jeffery_saarela(s: str) -> bool:
    pattern = r'\b(jeffery)\s*(m\.?)?\s*(saarela)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_terry_mcintosh(s: str) -> bool:
    pattern = r'\b(terry)\s*(t\.?)?\s*(mcintosh)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_william_cody(s: str) -> bool:
    pattern = r'\b(william)\s*(j\.?)?\s*(cody)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_fred_fodor(s: str) -> bool:
    pattern = r'\b(fred)\s*(fodor)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_charles_beil(s: str) -> bool:
    pattern = r'\b(charles)\s*(e\.?)?\s*(beil)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_curtis_bjork(s: str) -> bool:
    pattern = r'\b(curtis)\s*(r\.?)?\s*(bjork)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_jamie_fenneman(s: str) -> bool:
    pattern = r'\b(jamie)\s*(d\.?)?\s*(fenneman)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_erin_manton(s: str) -> bool:
    pattern = r'\b(erin)\s*(r\.?)?\s*(manton)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_adolf_ceska(s: str) -> bool:
    pattern = r'\b(adolf)\s*(ceska)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_oluna_ceska(s: str) -> bool:
    pattern = r'\b(oluna)\s*(ceska)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_le_taylor(s: str) -> bool: # updated 2024.10.24
    pattern = r'\b[l|e][l\.\s]*[e\.]*\s*ta[y|i]lorr*\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_john_pinder_moss(s: str) -> bool: # updated 2024.10.31
    pattern = r'\b(j|j.|john)?\s*(pinder)(-)?(moss)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_wilfred_schofield(s: str) -> bool:
    pattern = r'\b(wilfred)\s*(schofield)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_corinne_selby(s: str) -> bool:
    pattern = r'\b(corinne)\s*(j\.?)?\s*(selby)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_db_o_savile(s: str) -> bool:
    pattern = r'\b(d\.?b\.?o\.?)?\s*(savile)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_eli_wilson(s: str) -> bool:
    pattern = r'\b(eli)\s*(wilson)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_linda_jennings(s: str) -> bool:
    pattern = r'\b(l.|linda)\s*([p|.])*\s*(jenning(s)?|lipsen)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))

def match_quentin_cronk(s: str) -> bool:
    pattern = r'\b(q|quentin)\s*(cron(k|k)?|cronk)\b'
    return bool(re.search(pattern, s.strip(), re.IGNORECASE))
  
