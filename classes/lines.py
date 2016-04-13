import numpy as np

def closestDistanceBetweenLines(a0,a1,b0,b1,clampAll=False,clampA0=False,clampA1=False,clampB0=False,clampB1=False):
    ''' Given two lines defined by numpy.array pairs (a0,a1,b0,b1)
        Return distance, the two closest points, and their average
    '''

    # If clampAll=True, set all clamps to True
    if clampAll:
        clampA0=True
        clampA1=True
        clampB0=True
        clampB1=True

    # Calculate denomitator
    A = a1 - a0
    B = b1 - b0

    _A = A / np.linalg.norm(A)
    _B = B / np.linalg.norm(B)
    cross = np.cross(_A, _B);

    denom = np.linalg.norm(cross)**2


    # If denominator is 0, lines are parallel: Calculate distance with a projection
    # and evaluate clamp edge cases
    if (denom == 0):
        d0 = np.dot(_A,(b0-a0))
        d = np.linalg.norm(((d0*_A)+a0)-b0)

        # If clamping: the only time we'll get closest points will be when lines don't overlap at all.
        # Find if segments overlap using dot products.
        if clampA0 or clampA1 or clampB0 or clampB1:
            d1 = np.dot(_A,(b1-a0))

            # Is segment B before A?
            if d0 <= 0 >= d1:
                if clampA0 == True and clampB1 == True:
                    if np.absolute(d0) < np.absolute(d1):
                        return b0,a0,np.linalg.norm(b0-a0)
                    return b1,a0,np.linalg.norm(b1-a0)

            # Is segment B after A?
            elif d0 >= np.linalg.norm(A) <= d1:
                if clampA1 == True and clampB0 == True:
                    if np.absolute(d0) < np.absolute(d1):
                        return b0,a1,np.linalg.norm(b0-a1)
                    return b1,a1,np.linalg.norm(b1,a1)

        # If clamping is off, or segments overlapped, we have infinite results, just return position.
        return None,None,d



    # Lines criss-cross: Calculate the dereminent and return points
    t = (b0 - a0);
    det0 = np.linalg.det([t, _B, cross])
    det1 = np.linalg.det([t, _A, cross])

    t0 = det0/denom;
    t1 = det1/denom;

    pA = a0 + (_A * t0);
    pB = b0 + (_B * t1);

    # Clamp results to line segments if needed
    if clampA0 or clampA1 or clampB0 or clampB1:

        if t0 < 0 and clampA0:
            pA = a0
        elif t0 > np.linalg.norm(A) and clampA1:
            pA = a1

        if t1 < 0 and clampB0:
            pB = b0
        elif t1 > np.linalg.norm(B) and clampB1:
            pB = b1

    d = np.linalg.norm(pA-pB)

    return pA,pB,d