import gmpy2

# This too big?
gmpy2.get_context().precision=1000000

def printSmallest(p, q):
    if q < p:
        print(q)
    else:
        print(p)

    # Spaces out answers
    print()

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

    return p, q, N

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
    """
    Valid when |3p - 2q| < N^(1/4)

    Solving
    >>> 6N = A^2 - i^2 - A + i
    

    >>> [ax^2 + bx + c              = 0]
    >>>  1i^2 - 1i - (A^2 - A - 6N) = 0

    Therefore:

        a = 1
        b = -1
        c = (A^2 - A - 6N)
    """

    print("> Challenge 3")
    N = 720062263747350425279564435525583738338084451473999841826653057981916355690188337790423408664187663938485175264994017897083524079135686877441155132015188279331812309091996246361896836573643119174094961348524639707885238799396839230364676670221627018353299443241192173812729276147530748597302192751375739387929
    A = gmpy2.ceil(gmpy2.sqrt(6*N))
    
    a = gmpy2.mpz(1)
    b = gmpy2.mpz(-1)
    c = gmpy2.mpz(-(A**2 - A - 6*N))

    # Solving using quadratic formula
    # 
    #   x = (-b (+/-) b^2 - 4ac) / 2a
    #
    # b^2 - 4ac
    det = gmpy2.isqrt(b**2 - 4*a*c)

    plus = gmpy2.div(-b + det, 2*a)
    minus = gmpy2.div(-b - det, 2*a)

    answers = [plus, minus]

    for i in answers:

        # check for correct answer
        p = gmpy2.mpz(gmpy2.div(A + i - 1, 3))
        q = gmpy2.mpz(gmpy2.div(A - i, 2))

        # values found
        if p*q == N:
            printSmallest(p, q)

            return


    raise(Exception("[Challenge 3] > Could not find p or q"))

def num_to_string(no):
    nodig = no.digits(256)
    return "".join(map(chr, nodig))

def challenge4(RSAValues):
    """
    RSA Decryption challenge. Use previously found values of q and p to decrypt a provided message
    """

    print("> Challenge 4")
    e = gmpy2.mpz(65537)
    c = gmpy2.mpz(22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540)

    # Runs challenge 1 again to obtain the values
    p, q, N = RSAValues

    Nphi = gmpy2.mpz((p - 1)*(q - 1))

    # Private key generation
    d = gmpy2.invert(e, Nphi)

    m = gmpy2.powmod(c, d, N)
    m = gmpy2.to_binary(m)[::-1]
    
    
    # PKCS1
    printing = False
    
    for byte in m:

        # Split character used here is \x00
        if byte == 0: printing = True
        if printing: print(chr(byte), end='') 

    print()

if __name__ == "__main__":
    x = challenge1()
    challenge2()
    challenge3()
    challenge4(x)