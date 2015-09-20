import time
from urllib2 import urlopen as open
from BeautifulSoup import BeautifulSoup as bs
from urlparse import parse_qs

_url = 'http://www.hacker.org/runaway/index.php?name=aaa&password=bbb&path='

def map2mini(map,bx,by):
    out = {}
    for y in range(by):
        out[y]={}
        for x in range(bx):
            out[y][x]='.'
            rx = x
            ry = y
            while map.get(ry,{}).get(rx) and out[y][x]=='.':
                if map.get(ry,{}).get(rx)=='X':
                    out[y][x]='X'
                rx=rx+bx-1
                ry=ry+by-1
    return out

def fire(map,bx,by):
    path = {(0,0):''}
    do = 1
    while do>0:
        do = 0
        for k,v in path.items():
            if k==(by-1,bx-1):
                return path[k]
            else:
                path.pop(k)
            y = k[0]
            x = k[1]
            if map.get(y,{}).get(x+1)=='.' and (y,x+1) not in path:
                path[(y,x+1)]=v+'R'
                do = 1
            if map.get(y+1,{}).get(x)=='.' and (y+1,x) not in path:
                path[(y+1,x)]=v+'D'
                do = 1
    return path.get((by-1,bx-1),'')

def str2map(_str,bx,by):
    x = 0
    y = 0
    out = {}
    while _str:
        if x==0:
            out[y]={}
        out[y][x] = _str[0]
        _str = _str[1:]
        x+=1
        if x==bx:
            y+=1
            x=0
    return out

def do(begin=''):
    '''
    >>> from urlparse import parse_qs
    >>> parse_qs(w)
    u'FVlevel': [u'4'], 
    u'FVboardX': [u'5'], 
    u'FVboardY': [u'5'], 
    u'FVinsMax': [u'3'], 
    u'FVinsMin': [u'2'], 
    u'FVterrainString': [u'.XX............XX.X....XX']}
        >>> w
    u'FVterrainString=.XX............XX.X....XX&FVinsMax=3&FVinsMin=2&FVboardX=5&FVboardY=5&FVlevel=4'
    '''
    doc = open(_url+begin).readlines()
    #================================  level 100
    html = ''.join(doc)
    _list = html.split('<!--')[1]
    doc = _list.split('-->')[0]
    #================================  level 100
    soup = bs(''.join(doc))
    for one in soup.findAll(attrs={'name':'FlashVars'}):
        d = parse_qs(one.get('value'))
    level = int(d[u'FVlevel'][0])
    insMin = int(d[u'FVinsMin'][0])
    insMax = int(d[u'FVinsMax'][0])
    boardX = int(d[u'FVboardX'][0])
    boardY = int(d[u'FVboardY'][0])
    _map = d[u'FVterrainString'][0]
    map = str2map(_map,boardX,boardY)
    print "level %d"%level
    _begin = time.time()
    path = ''
    for n in range(insMin,insMax+1):
        for x in range(1,n+2):
            y = n+2-x
            mini = map2mini(map,x,y)
            path = fire(mini,x,y)
            if path:break
        if path:break
    print "time ",time.time()-_begin
    print("level %d path is [ %s ]"%(level,path))
    do(path)                