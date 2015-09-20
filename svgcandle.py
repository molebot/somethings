import time

funcs = {
"aa":aa,        # func from outside import here
        }

class SVG:
    height  = 400.0     #       400.0
    block   = 10        #       8
    width   =   6       #       6
    half    =   3       #       3
    center  = 5         #       4
    border  = 1         #       1
    margin  = 10        #       10
    up      =   (220,0,0)
    dn      =   (0,128,0)
    eq      =   (74,182,198)
    red     =   (255,0,0)
    yellow  =   (255,255,0)
    green   =   (0,200,0)
    blue    =   (0,0,255)
    grey    =   (100,100,100)
    grey2    =   (200,200,200)
    timecolor = [(255,  255,    0,   ),
                 (128,  128,    0,   ),
                 (0,    255,    255, ),
                 (255,  0,      255, ),
                 (0,    128,    128, ),
                 (128,  0,      128, )]
    lines   = {
                "show":[
                      ("fox",           blue,   True,   "ss"),
                      ("point",         grey,   False,  "ohlc"),
                      ("line_aa_3_1_0", red,    True,   "ss"),
                      ("const_a", 12,   green,  True,   "ss"),
                   ],
        }
    def to_html(self):
#        logger.error('a%.3f'%time.time())
        self.make_k()
#        logger.error('b%.3f'%time.time())
        out = []
        n = 1
        for i in self.txt:
            out.append(self.text(i,1,self.height-n*15,"red"))
            n+=1
        out.append('<!--draw percent-->')
        out.append(self.draw_percent())
        out.append('<!--draw ohlc-->')
        out.append(self.draw_ohlc())
        out.append('<!--draw lines-->')
        out.append(self.draw_lines())
#        out.append("<br/>")
#        out.append("<br/>")
        return self.svg(''.join(out))
    def draw_ohlc(self):
        out = []
        for i in xrange(len(self.data)):
            one = self.data[i]
            _hour = int(float(one['time'])/3600)%6
            color = self.timecolor[_hour]
            o = self.magic_y(one['o'],'ohlc')
            h = self.magic_y(one['h'],'ohlc')
            l = self.magic_y(one['l'],'ohlc')
            c = self.magic_y(one['c'],'ohlc')
            out.append(self.draw_time_color(i,color)+self.ohlc(i,o,h,l,c))
        return ''.join(out)
    def draw_percent(self):
        out = []
        _num = len(self.data)
        style = "fill:none;stroke:rgb(%d,%d,%d);stroke-width:1"%self.grey2
        for i in xrange(1,8):
            out.append(self.line([(0,i*self.height/8),(_num*self.block,i*self.height/8.0)],style))
        n = 0
        for ks in self.k.keys():
            k = self.k[ks]
            _min = self.min[ks]
            for j in xrange(1,8):
                out.append(self.text('%s=%.1f'%(ks,k*(self.height-(8-j)*self.height/8.0)+_min),200+100*n,1+j*self.height/8.0,"grey"))
            n+=1
        return ''.join(out)
    def draw_lines(self):
        out = []
        for k,v in self.out.items():
            tag = k[-1]
            color = k[-3]
            style = "fill:none;stroke:rgb(%d,%d,%d);stroke-width:1"%color
            _min = self.min[tag]
            k = self.k[tag]
            data = []
            i = 0
            for o in v:
                center = i*self.block+self.border+self.half
                y = (o-_min)/k
                data.append((center,y))
                i+=1
            out.append(self.line(data,style))
        return ''.join(out)
    def ohlc(self,pos,o,h,l,c):
        center = pos*self.block+self.border+self.half
        x = pos*self.block+self.border
        if c-o>0.1:
            clr = self.up
            rect = self.rect([(x,c),(x,o),(x+self.width,o),(x+self.width,c)],
                             "fill:rgb(%d,%d,%d);stroke:none;"%clr,"k")
        elif o-c>0.1:
            clr = self.dn
            rect = self.rect([(x,o),(x,c),(x+self.width,c),(x+self.width,o)],
                             "fill:rgb(%d,%d,%d);stroke:none;"%clr,"k")
        else:
            clr = self.eq
            rect = self.rect([(x,o),(x,o+1),(x+self.width,o+1),(x+self.width,o)],
                             "fill:rgb(%d,%d,%d);stroke:none;"%clr,"k")
        line = self.line([(center,h),(center,l)],"fill:none;stroke:rgb(%d,%d,%d);stroke-width:1"%clr)
        return line+rect
    def draw_time_color(self,pos,color):
        x = pos*self.block
        return self.rect([
            (x,self.height/2+2),
            (x,self.height/2-2),
            (x+self.block,self.height/2-2),
            (x+self.block,self.height/2+2)
                     ],"fill:rgb(%d,%d,%d);stroke:none"%color,"color")
    def text(self,t,x,y,fill):
        return '''<text x="%d" y="%.2f" fill="%s">%s</text>'''%(x,self.re_y(y),fill,t)
    def line(self,lines,style):
        ps = map(lambda x:'%d %.2f'%(x[0],self.re_y(x[1])),lines)
        xy = ' '.join(ps)
        return '''<polyline points="%s" style="%s"/>'''%(xy,style)
    def rect(self,points,style,tag):
        ps = map(lambda x:'%d %.2f'%(x[0],self.re_y(x[1])),points)
        xy = ' L'.join(ps)
        return '''<path d="M%s Z" style="%s" class="%s"/>'''%(xy,style,tag)
    def make_k(self):
        tmp = {}
        for o in self.data:
            self.max['ohlc'] = max(self.max.get('ohlc',o['h']+10),o['h'])
            self.min['ohlc'] = min(self.min.get('ohlc',o['l']-10),o['l'])
            self.k['ohlc'] = 0
            for one in self.group:
                k = one[0]
                value = tmp.get(k,0.0)
                if k in o:
                    value = o[k]
                elif k[0]=='-' and k[1:] in o:
                    value = -1*o[k[1:]]
                else:
                    if 'line' in k:
                        _line,_type,_pos,_un,_v = k.split("_")
                        _pos = int(_pos)
                        _un = int(_un)
                        _v = int(_v)
                        value = funcs[_type](_pos,o,_un,3,_v*(1+myth))
                    elif 'const' in k:
                        value = one[1]
                    o[k] = value
                tmp[k] = value
                _l = self.out.get(one,[])
                _l.append(value)
                self.out[one] = _l
                if one[-2]:
                    self.max[one[-1]] = max(self.max.get(one[-1],   abs(value)),   abs(value))
                    self.min[one[-1]] = min(self.min.get(one[-1],-1*abs(value)),-1*abs(value))
                else:
                    self.max[one[-1]] = max(self.max.get(one[-1],value),value)
                    self.min[one[-1]] = min(self.min.get(one[-1],value),value)
                self.k[one[-1]] = 0
        for ks in self.k.keys():
            self.max[ks]+=1
            self.min[ks]-=1
            self.k[ks] = max(0.001,(self.max[ks]-self.min[ks])/self.height)
    def __init__(self,pos,datalist,textlist,data):
        self.txt = textlist
        self.len = len(datalist)
        self.group = self.lines[pos]
        self.data = datalist
        self.db = data
        self.max = {}
        self.min = {}
        self.k = {}
        self.out = {}
    def re_y(self,v):return self.height-v
    def magic_y(self,v,tag):return (v-self.min[tag])/self.k[tag]
    def svg(self,l):
        return '''<svg width="%d" height="500" xmlns="http://www.w3.org/2000/svg" version="1.1"><g>'''%max(400,self.len*self.block)+l+'''</g></svg>'''
