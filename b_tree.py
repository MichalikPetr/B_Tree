import random

def make_tree(t):
    return [[], [], t]

def get_keys(tree):
    return tree[0]

def get_children(tree):
    return tree[1]

def get_t(tree):
    return tree[2]

def set_keys(tree, keys):
    tree[0] = keys

def set_children(tree, children):
    tree[1] = children

def set_t(tree, t):
    tree[2] = t

def tree_search(tree, n):
    """Funkce prohledá strom a vrací podstrom s hledaným číslem a jeho index. Pokud strom ćíslo neobsahuje, vrací hodnotu False."""
    i = 0
    key_amount = len(get_keys(tree))

    while i < key_amount and n > get_keys(tree)[i]:
        i += 1
    
    if i < key_amount and n == get_keys(tree)[i]:
        return tree, i
    
    elif get_children(tree) == []:
        return False
    
    else:
        return tree_search(get_children(tree)[i], n)

"""
Prvek stromu je definován seznamem seznamů, kdy prvním seznamem jsou klíče a druhým seznamem jsou potomci
"""


"""
strom = [[11], [
            [[9], [
                [[8], []],
                [[10], []]]],
            [[16, 18], [
                [[15], []],
                [[17], []],
                [[20, 23], []]]]]]

print(tree_search(strom, 16))
print(tree_search(strom, 23))
print(tree_search(strom, 2))
"""

def format_tree(tree, level, ftree):
    """Vrací strom v tisknutelném formátu."""
    if len(ftree) - 1 < level:
        ftree += [[get_keys(tree)]]
    else:
        ftree[level] += [get_keys(tree)]

    for child in get_children(tree):
        format_tree(child, level + 1, ftree)
    return ftree

def print_tree(tree):
    """Vytiskne strom"""
    ftree = format_tree(tree, 0, [])
    for level in ftree:
        print(level)

"""
strom = [[11], [
            [[9], [
                [[8], []],
                [[10], []]]],
            [[16, 18], [
                [[15], []],
                [[17], []],
                [[20, 23], []]]]]]

print_tree(strom)
print_tree(get_children(strom)[1])
"""

def split_child(x, i):
    """Rozdělí podstrom x na indexu i"""
    t = get_t(x)                                                                    #parametr t
    z = make_tree(t)                                                                #vytvoří nový prázdný strom
    y = list(get_children(x)[i])                                                    #vezme podstrom na indexu i

    xkeys = get_keys(x)                                                             #vezme klíče z původního stromu
    xkeys.insert(i, get_keys(y)[t - 1])                                             #na index i vloží prostřední klíč z potomka

    set_keys(z, get_keys(y)[t:])                                                    #do z dá prvky z podstromu od indexu t
    set_keys(y, get_keys(y)[:t - 1])                                                #do y dá prvky z podstromu po index t - 1

    if get_children(y) != []:                                                       #pokud podstrom obsahoval potomky
        ychildren = get_children(y)                                                 #vezme potomky

        set_children(z, ychildren[t:])                                              #do z vloží potomky od indexu t (pravou část)
        set_children(y, ychildren[:t])                                              #do y vloží potomky po index t (levou část)

    xchildren = get_children(x)                                                     #vezme potomky
    xchildren[i] = y                                                                #levé potomky nastaví na y
    xchildren.insert(i + 1, z)                                                      #vloží pravé potomky

    set_keys(x, xkeys)                                                              #původí klíče nahradí novými
    set_children(x, xchildren)                                                      #původní potomky nahradí novými


def insert_nonfull(x, k):
    """Vloží prvek k do stromu x. Předpokládá, že kořen není zaplněný"""
    n = len(get_keys(x))                                                            #délka stromu
    i = n - 1                                                                       #index od konce
    t = get_t(x)                                                                    #parametr t

    if get_children(x) == []:                                                       #pokud je list
        get_keys(x).append(None)                                                    #vloží se prázdný prvek na konec
        while i >= 0 and k < get_keys(x)[i]:                                        #dokud je k menší, než klíč na indexu i a dokud není na nazačátku
            get_keys(x)[i + 1] = get_keys(x)[i]                                     #posouvá prvky doprava
            i -= 1
        get_keys(x)[i + 1] = k                                                      #na získaném indexu vloží prvek

    else:                                                                           #pokud není list
        while i >= 0 and k < get_keys(x)[i]:                                        #hledá správný podstrom pomocí klíčů
            i -= 1
        i += 1

        if len(get_keys(get_children(x)[i])) == 2 * t - 1:                          #pokud je daný podstrom plný
            split_child(x, i)                                                       #preventivně se rozdělí
            if k > get_keys(x)[i]:                                                  #ověří se, do kterého z nových podstromů patří
                i += 1
        insert_nonfull(get_children(x)[i], k)                                       #provede vložení do podstromu


def insert(x, k):
    """Pokud je kořen zaplněný, rozdělí ho a vloží prvek do stromu."""
    n = len(get_keys(x))                                                            #délka kořene
    t = get_t(x)                                                                    #parametr t
    if n == 2 * t - 1:                                                              #pokud je kořen plný
        s = make_tree(t)                                                            #vytvoří se nový strom
        set_children(s, [x])                                                        #do potomka se vloží původní strom
        split_child(s, 0)                                                           #ten se rozdělí
        insert_nonfull(s, k)                                                        #do něj se vloží k

        set_keys(x, get_keys(s))                                                    #nový strom přepíše původní
        set_children(x, get_children(s))
        
    else:
        insert_nonfull(x, k)                                                        #pokud není kořen plný, pouze se prvek vloží



#TEST INSERTU
"""
strom = make_tree(3)                                                                #VYTVOŘÍ NOVÝ STROM

numlist = []                                                                        #VYTVOŘÍ SEZNAM
for i in range(1, 26):
    numlist += [i]                                                                  #VLOŽÍ DO SEZNAMU ČÍSLA 1 - 25

random.shuffle(numlist)                                                             #NÁHODNĚ ZAMÍCHÁ SEZNAM

for i in numlist:                                                                   #VLOžÍ ČÍSLA ZE SEZNAMU
    insert(strom, i)

print_tree(strom)                                                                   #VYPÍŠE SEZNAM
"""

def rotate_left(x, i):
    """Provede rotaci vlevo."""
    y = get_children(x)[i]                                                          #levý podstrom
    z = get_children(x)[i + 1]                                                      #pravý podstrom

    tempkeys = get_keys(y)                                                          #vezme klíče v levém podstromu
    tempkeys += [get_keys(x)[i]]                                                    #přidá k nim klíč ze stromu na indexu i
    set_keys(y, tempkeys)                                                           #nastaví klíče do levého podstromu

    zkey = get_keys(z)[0]                                                           #vezme nejmenší prvek z pravého podstromu
    get_keys(x)[i] = zkey                                                           #nastaví do stromu x daný prvek
    del get_keys(z)[0]                                                              #z pravého podstromu prvek odstraní

    if get_children(z) != []:                                                       #pokud pravý podstrom obsahuje potomky
        zchild = get_children(z)[0]                                                 #vezme prvního potomka pravého podstromu
        del get_children(z)[0]                                                      #odstraní ho z něj
        ychildren = get_children(y)
        ychildren += zchild                                                         #přidá ho do levého podstromu

def rotate_right(x, i):
    """Provede rotaci vpravo."""
    y = get_children(x)[i + 1]                                                      #pravý podstrom
    z = get_children(x)[i]                                                          #levý podstrom

    tempkeys = get_keys(y)                                                          #klíče v pravém podstromu
    tempkeys.insert(0, get_keys(x)[i])                                              #přidá k nim klíč z x na indexu i
    set_keys(y, tempkeys)                                                           #nastaví klíče

    zlen = len(get_keys(z))                                                         #počet klíčů v z
    zkey = get_keys(z)[zlen - 1]                                                    #největší klíč levého podstromu
    get_keys(x)[i] = zkey                                                           #nastaví ho do x
    del get_keys(z)[zlen - 1]                                                       #odstraní ho z levého podstromu

    if get_children(z) != []:
        zchild = get_children(z)[zlen - 1]
        del get_children(z)[zlen - 1]
        ychildren = get_children(y)
        ychildren.insert(0, zchild)

#TEST ROTACÍ
"""
strom = [[6, 10, 16, 21], [[[1, 2, 3, 4, 5], [], 3], [[7, 8, 9], [], 3], [[11, 12, 13, 14, 15], [], 3], [[17, 18, 19, 20], [], 3], [[22, 23, 24, 25], [], 3]], 3]
print("s1:")
print_tree(strom)
rotate_left(strom, 1)
print("s2:")
print_tree(strom)
rotate_right(strom, 1)
print("s3:")
print_tree(strom)
"""


def merge_right(x, i):
    """Spojí minimální potomky."""
    y = get_children(x)[i]                                                          #levý podstrom
    z = list(get_children(x)[i + 1])                                                #pravý podstrom (kopie)

    xkey = get_keys(x)[i]                                                           #klíč z x si uloží bokem
    del get_keys(x)[i]                                                              #a odstraní ho z x

    ykeys = get_keys(y)
    ychildren = get_children(y)
    ykeys += [xkey]                                                                 #vloží klíč do levého podstromu
    ykeys += get_keys(z)                                                            #vloží do levého podstromu pravý podstrom
    ychildren += get_children(z)
    del get_children(x)[i + 1]                                                      #odstraní pravý podstrom z x

#TEST MERGE
"""
strom = [[6, 10, 16, 21], [[[1, 2, 3, 4, 5], [], 3], [[7, 8, 9], [], 3], [[11, 12, 13, 14, 15], [], 3], [[17, 18, 19, 20], [], 3], [[22, 23, 24, 25], [], 3]], 3]
print("s1:")
print_tree(strom)
merge_right(strom, 1)
print("s2:")
print_tree(strom)
"""


def delete_predecessor(x, k):
    """Najde největší prvek levého podstromu"""
    n = len(get_keys(x)) 
    if get_children(x) == []:                                                       #pokud je v listu                                                
        num = get_keys(x)[n - 1]                                                    #poslední klíč
        del get_keys(x)[n - 1]                                                      #odstraní ho
        return num                                                                  #vrátí ho
    else:
        t = get_t(x)
        child = get_children(x)[n - 1]                                              #podívá se do potomka
        if len(get_keys(child)) < t:                                                #pokud je potomek minimální
            leftchild = get_children(x)[n - 2]                                      #vezme levý potomek
            if len(get_keys(leftchild)) < t:                                        #pokud je i levý potomek minimální
                merge_right(x, n - 1)                                               #spojí je
                return delete_predecessor(get_children(x)[n - 2], k)                #zavolá funkci na potomka (index se posune, protože se potomci spojí)
            else:                                                                   #pokud ne
                rotate_right(x, n - 1)                                              #provede rotaci vpravo
                return delete_predecessor(get_children(x)[n - 1], k)                #zavolá funkci na potomka
        else:                                                                       #pokud potomek není minimální
            return delete_predecessor(get_children(x)[n - 1], k)                    #zavolá funkci na potomka

def delete_rpredecessor(x, k):
    """Najde nejmenší prvek pravého podstromu."""
    n = len(get_keys(x))
    if get_children(x) == []:
        num = get_keys(x)[0]
        del get_keys(x)[0]
        return num
    else:
        t = get_t(x)
        child = get_children(x)[0]
        if len(get_keys(child)) < t:
            rchild = get_children(x)[1]
            if len(get_keys(rchild)) < t:
                merge_right(x, 0)
                return delete_rpredecessor(get_children(x)[0], k)
            else:
                rotate_left(x, 0)
                return delete_rpredecessor(get_children(x)[0], k)
        else:
            return delete_rpredecessor(get_children(x)[0], k)


def delete_nonminimal(x, k):
    """Odstraní prvek ze stromu. Předpokládá, že podstrom, ve kterém se prvek nachází, není minimální."""
    t = get_t(x)
    n = len(get_keys(x))
    i = n - 1

    while i >= 0 and k < get_keys(x)[i]:                                            #hledá podstrom, ve kterém se prvek nachází
        i -= 1
    i += 1

    if get_keys(x)[i - 1] == k:                                                     #pokud nalezne klíč, který chceme odstranit
        if get_children(x) == []:                                                   #pokud se klíč nachází v listu
            del get_keys(x)[i - 1]                                                  #odstraní ho
        else:
            """pro připad s kořenem"""
            leftchild = get_children(x)[i - 1]                                      #levý potomek
            if len(get_keys(leftchild)) < t:                                        #pokud je levý potomek minimální
                rightchild = get_children(x)[i]                                     #pravý potomek
                if len(get_keys(rightchild)) < t:                                   #pokud je minimální
                    merge_right(x, i - 1)                                           #dojde k mergi
                    if len(get_keys(x)) == 0:                                       #pokud se smaže celý kořen (byl v kořenu jen 1 prvek)
                        child = get_children(x)[0]                                  #vezme nový strom (ten mergenutý)
                        set_keys(x, get_keys(child))
                        set_children(x, get_children(child))
                        delete_nonminimal(x, k)

                    else:
                        delete_nonminimal(x, k)

                else:                                                               #pokud pravý potomek není minimální
                    get_keys(x)[i - 1] = delete_rpredecessor(get_children(x)[i], k) #najde nejmenší prvek pravého podstromu, kterým ho nahradí
            
            else:                                                                   #pokud levý potomek není minimální
                get_keys(x)[i - 1] = delete_predecessor(get_children(x)[i - 1], k)  #najde největší prvek levého podstromu, kterým ho nahradí
    
    
    else:
        sub = get_children(x)[i]                                                    #vezme podstrom, kde se může nacházet potomek
        if len(get_keys(sub)) < t:                                                  #pokud je podstrom minimální
            if i > 0:                                                               #pokud není podstrom ten nejvíce levý
                sub2 = get_children(x)[i - 1]
                if len(get_keys(sub2)) < t:                                         #pokud je i levý minimální
                    merge_right(x, i - 1)                                           #spojí je
                    delete_nonminimal(get_children(x)[i - 1], k)                    #zavolá funkci delete na potomka s indexem i - 1
                else:                                                               #pokud levý potomek není minimální
                    rotate_right(x, i - 1)                                          #provede rotaci vpravo
                    delete_nonminimal(get_children(x)[i], k)                        #zavolá funkci delete na potomka s indexem i

            else:                                                                   #pokud se prvek nachází v levém podstromu
                sub2 = get_children(x)[i + 1]                                       #podíváme se do pravého podstromu
                if len(get_keys(sub2)) < t:                                         #pokud je minimální
                    merge_right(x, i)                                               #merge
                    if len(get_keys(x)) == 0:                                       #pokud merge smaže všechny prvky kořenu
                        child = get_children(x)[0]                                  #shodí strom o úroveň
                        set_keys(x, get_keys(child))
                        set_children(x, get_children(child))
                        delete_nonminimal(x, k)
                    else:
                        delete_nonminimal(get_children(x)[i], k)
                else:
                    rotate_left(x, i)
                    delete_nonminimal(get_children(x)[i], k)
        
        else:                                                                       #pokud podstrom není minimální
            delete_nonminimal(get_children(x)[i], k)                                #zavolá fci





#POUŽITÍ PROGRAMU
"""
strom = make_tree(2)
#funkce make tree bere parametr t a vrací prázdný strom s daným parametrem

insert(strom, 20)
insert(strom, 50)
insert(strom, 30)
insert(strom, 60)
insert(strom, 40)
insert(strom, 55)
insert(strom, 70)
insert(strom, 90)
insert(strom, 10)
insert(strom, 15)
insert(strom, 5)
#funkce insert bere jako parametry strom a prvek, který do stromu chcete vložit

print_tree(strom)
print()
#fuknce print_tree vypíše strom do konzole
#na každém řádku je jedna úroveň stromu

delete_nonminimal(strom, 10)
delete_nonminimal(strom, 5)
#funkce delete_nonminimal odstraní ze stromu prvek
#(jméno bylo pracovní, proto je v něm to nonminimal)
print_tree(strom)
print()


#MŮJ TEST MAZÁNÍ CELÉHO STROMU

delete_nonminimal(strom, 50)
print_tree(strom)
print()
delete_nonminimal(strom, 60)
print_tree(strom)
print()
insert(strom, 60)
print_tree(strom)
print()
insert(strom, 80)
print_tree(strom)
print()
insert(strom, 100)
insert(strom, 110)
print_tree(strom)
print()


print("start")
delete_nonminimal(strom, 55)
print_tree(strom)
print()
delete_nonminimal(strom, 30)
print_tree(strom)
print()
delete_nonminimal(strom, 70)
print_tree(strom)
print()
delete_nonminimal(strom, 90)
print_tree(strom)
print()
delete_nonminimal(strom, 15)
print_tree(strom)
print()
delete_nonminimal(strom, 20)
print_tree(strom)
print()
delete_nonminimal(strom, 40)
print_tree(strom)
print()
delete_nonminimal(strom, 60)
print_tree(strom)
print()
delete_nonminimal(strom, 80)
print_tree(strom)
print()
delete_nonminimal(strom, 100)
print_tree(strom)
print()
delete_nonminimal(strom, 110)
print_tree(strom)
print()
"""