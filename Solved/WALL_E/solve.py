#!/usr/bin/env python3
import gmpy2


# Divide away the padding of 0x100 by adding modulo
# ... until the numerator is divisible by 0x100
# the check for divisibility is done by doing AND of 0xFF
def divide_away_padding(numerator, n):
    multiplicator = 0
    while True:
        #print('Iterate', multiplicator)
        x = numerator + multiplicator * n
        if (x & 0xFF) == 0:
            x //= 0x100
            break

        multiplicator += 1
    return (x, multiplicator)


# Do a division within the modulo. If final result is a fraction,
# then add the modulo to wrap around and try again.
def division_under_modulo(numerator, divisor, n):
    for tries in range(10000):
        # print('Iterate')
        result = numerator // divisor

        if result * divisor != numerator:
            numerator += n
        else:
            return result


# Do a cuberoot within the modulo.
def cuberoot_under_modulo(orig, n):
    # https://stackoverflow.com/a/356187
    # gmpy2 has gmpy2.iroot to compute integer roots
    # m = gmpy2.iroot(ct, 3)[0]
    for tries in range(10000):
        # print('Iterate')
        result = gmpy2.iroot(orig, 3)[0]

        if int(pow(result, 3)) == int(orig):
            return result
        else:
            orig += n

# Given parameters
n = 16930533490098193592341875268338741038205464836112117606904075086009220456281348541825239348922340771982668304609839919714900815429989903238980995651506801223966153299092163805895061846586943843402382398048697158458017696120659704031304155071717980681280735059759239823752407134078600922884956042774012460082427687595370305553669279649079979451317522908818275946004224509637278839696644435502488800296253302309479834551923862247827826150368412526870932677430329200284984145938907415715817446807045958350179492654072137889859861558737138356897740471740801040559205563042789209526133114839452676031855075611266153108409
c = 11517346521350511968078082236628354270939363562359338628104189053516869171468429130280219507678669249746227256625771360798579618712012428887882896227522052222656646536694635021145269394726332158046739239080891813226092060005024523599517854343024406506186025829868533799026231811239816891319566880015622494533461653189752596749235331065273556793035000698955959016688177480102004337980417906733597189524580640648702223430440368954613314994218791688337730722144627325417358973332458080507250983131615055175113690064940592354460257487958530863702022217749857014952140922260404696268641696045086730674980684704510707326989
e = 3

# Bruteforce division of padding bytes
ct = c
for P in range(0, 1000):
    print('Try padding:', P)
    '''
    pt_padding = pow(0x100, P)
    ct_padding = pow(pt_padding, e)
    # divide away the padding, slow
    ct = division_under_modulo(c, ct_padding, n)
    '''

    # divide away the padding, efficiently
    ct, multiplicator = divide_away_padding(ct, n)

    # cuberoot within the modulo
    m = cuberoot_under_modulo(ct, n)
    if m == None:
        continue

    # decrypt
    try:
        flag = bytes.fromhex('%x' % m)
    except:
        flag = bytes.fromhex('0%x' % m)

    print(flag)
    if b'actf' in flag:
        print(flag.decode())
        quit()
