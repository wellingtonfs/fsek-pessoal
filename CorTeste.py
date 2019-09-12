def Conversao2hsv(x,y,z):
    x = float(r/255.0)
    y = float(g/255.0)
    z = float(b/255.0)

    mx = max(x, y, z)
    mn = min(x, y, z)
    dif = float(mx - mn)
    if mx == mn: 
        h = 0
    elif mx == x:
        h = float((60 * ((y-z)/dif) + 360) % 360)
    elif mx == y:
        h = float((60 * ((z-x)/dif) + 120) % 360)
    elif mx == z:
        h = float((60 * ((x-y)/dif) + 240) % 360)
    if mx == 0:
        s = 0
    else:
        s = float(100*dif/mx)
    v = float(100*mx)
    return (h,s,v)

def Conversao2rgb(h,s,v):
    h = float(hsv[0])
    s = float(hsv[1]/100)
    v = float(hsv[2]/100)

    hi = h/60
    c = float(v*s)
    x = float(c*(1 - abs(((hi)%2)-1)))
    m = float(v-c)

    if 0 <= hi <= 1:
        ri, gi, bi = c, x, 0
    if 1 < hi <= 2:
        ri, gi, bi = x, c, 0
    if 2 < hi <= 3:
        ri, gi, bi = 0, c, x
    if 3 < hi <= 4:
        ri, gi, bi = 0, x, c 
    if 4 < hi <= 5:
        ri, gi, bi = x, 0, c  
    if 5 < hi <= 6:
        ri, gi, bi = c, 0, x  

    x = round((ri + m))
    y = round((gi + m))
    z = round((bi + m))

    return (x,y,z)