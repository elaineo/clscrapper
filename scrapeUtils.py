import unicodedata
import string
from cllocs import *

def parse_locs(title, descr):
    #start = 'Mountain View, CA'
    #dest = 'Los Angeles, CA'
    start = None
    dest = None
    
    titletxt = unicodedata.normalize('NFKD', title).encode('ascii','ignore')
    descrtxt = unicodedata.normalize('NFKD', descr).encode('ascii','ignore')
    
    titletxt = titletxt.lower().split()
    descrtxt = descrtxt.lower().split()

    to_ind = [i for i, x in enumerate(titletxt) if x == " to "]
    
    # destination
    for i in to_ind:        
        try:
            target_dest = titletxt[i+1]
            if target_dest.lower() in LocPrefixes:
                target_dest = titletxt[i+1] + titletxt[i+2]
        except:
            continue
        if target_dest in CLDests:
            dest = CLDests[target_dest]
            continue            
        elif target_dest in CLBayArea:
            dest = CLBayArea[target_dest]
            continue
    if not dest:
        for loc in CLDests:
            if loc.lower() in title.lower():
                dest = CLDests[loc]
                continue
    if not dest:
        for loc in CLDests:
            if loc.lower() in descr.lower():
                dest = CLDests[loc]
                continue

    if not dest:
        dest = 'Los Angeles, CA'                
    
    # origin. start with stuff in parens
    try:
        paren_start = title.index( '(' )
        paren_end = title.index( ')', paren_start )
        from_locs =  title[paren_start+1:paren_end].split(' / ')
    except ValueError:
        from_locs = []                
        
    
    if len(from_locs) > 0:
        if from_locs[0] in SFHoods:
            start = 'San Francisco, CA'
        elif from_locs[0] in CLBayArea:
            start = CLBayArea[from_locs[0]]
        else:
            for loc in CLBayArea:
                if loc.lower() in from_locs[0].lower():
                    start = CLBayArea[loc]
                    continue              

    if start:
        return start, dest
        
    descrtxt.append(titletxt)
    from_ind = [i for i, x in enumerate(descrtxt) if x == " from "]   
        
    for i in from_ind:
        try:
            target_start = descrtxt[i+1]
            if target_start.lower() in LocPrefixes:
                target_start = descrtxt[i+1] + descrtxt[i+2]
        except:
            continue
        
        if target_start in CLBayArea:
            start = CLBayArea[target_start]
            continue
    if not start:
        for loc in CLBayArea:
            if loc.lower() in descr.lower():
                start = CLBayArea[loc]
                continue              

    if not start:
        start = 'San Francisco, CA'

    return start, dest
    

def parse_wanted(descr):
    for n in needy:
        if string.find(descr.lower(), n) != -1:
            return True
    return False
    