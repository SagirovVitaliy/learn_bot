import ephem

# print(ephem._libastro.builtin_planets())

b = 'pluto'


b = ([name for m, x, name in ephem._libastro.builtin_planets()])



print(b[:8])

#if b in k:
    #print('da')