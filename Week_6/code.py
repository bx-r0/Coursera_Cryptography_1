import math
import decimal
import gmpy2

# This too big?
gmpy2.get_context().precision=1000000

def printSmallest(p, q):
    if q < p:
        print(q)
    else:
        print(p)

def challenge1():

    print("> Challenge 1")
    N = 179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581
    N_sqrt = gmpy2.sqrt(N)

    # A = round(√N)
    A = gmpy2.ceil(N_sqrt)

    # x = √(A^2 - N)
    x = gmpy2.sqrt(pow(A, 2) - N)

    p = A - x
    q = A + x

    printSmallest(p, q)

def challenge2():
    """
    Uses Fermant factorisation
    """

    print("> Challenge 2")
    N = 648455842808071669662824265346772278726343720706976263060439070378797308618081116462714015276061417569195587321840254520655424906719892428844841839353281972988531310511738648965962582821502504990264452100885281673303711142296421027840289307657458645233683357077834689715838646088239640236866252211790085787877
    
    N_sqrt = gmpy2.sqrt(N)

    A = gmpy2.ceil(N_sqrt)
    b2 = A * A - N

    while not gmpy2.is_square(gmpy2.mpz(b2)):

        A = A + 1
        b2 = A * A - N

    # Works out p and q
    q = A - gmpy2.sqrt(b2)
    p = N / q

    printSmallest(p, q)

def challenge3():
    pass

if __name__ == "__main__":
    challenge1() # Submit without the .0
    challenge2()