import gmpy2

gmpy2.get_context().precision=1530

def challenge(p, g, h):

    # Equation:
    #   [h/g^(x1) = (g^B)^x0] in Zp

    B = pow(2, 20)

    # Compute hash table of values for:
    #   h/g^(x1)
    hashTableX1 = {}
    for x1 in range(B):
        x = gmpy2.divm(h, gmpy2.powmod(g, x1, p), p)
        hashTableX1[x] = x1

    print("Pre compute complete!")

    # Compare values by computing
    #   (g^B)^x0
    for x0 in range(B):
        t = gmpy2.mpfr(gmpy2.powmod(gmpy2.powmod(g, B, p), x0, p)) % p

        if t in hashTableX1:

            x1 = hashTableX1[t]

            # Calculates x
            x = x0 * B + x1

            print("Value found!")
            print(x)
            break
    else:
        print("## No value found! ##")
    

if __name__ == "__main__":
 
    p = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171
    g = 11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568
    h = 3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333
    
    challenge(p, g, h)