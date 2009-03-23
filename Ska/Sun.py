"""
Utility for calculating sun position.
"""

from math import pi,sin,cos,atan2,asin

def position( julian_date ):
    """
    Calculate the sun position at the given Julian date.

    Code modified from http://idlastro.gsfc.nasa.gov/ftp/pro/astro/sunpos.pro

    Example::
    
     >>> import Ska.Sun
     >>> import Chandra.Time
     >>> jd = Chandra.Time.DateTime('2008:002:00:01:02').jd
     >>> Ska.Sun.position(jd)
     (281.90344855695275, -22.9892737322084)

    :param julian_date: Input Julian date.
    :rtype: RA, Dec in decimal degrees (J2000).
    """
    jd = julian_date
    
    t = (jd - 2415020)/(36525.0)

    dtor = pi/180

# sun's mean longitude
    l = ( 279.696678 + ((36000.768925*t) % 360.0) )*3600.0

# Earth anomaly
    me =  358.475844 + (35999.049750*t) % 360.0
    ellcor = (6910.1 - (17.2*t))*sin(me*dtor) + 72.3*sin(2.0*me*dtor)
    l = l + ellcor
    
## allow for the Venus perturbations using the mean anomaly of Venus MV
    mv = 212.603219 + (58517.803875*t) % 360.0
    vencorr = 4.8 * cos((299.1017 + mv - me)*dtor) + \
        5.5 * cos((148.3133 +  2.0 * mv  -  2.0 * me )*dtor) + \
        2.5 * cos((315.9433 +  2.0 * mv  -  3.0 * me )*dtor) + \
        1.6 * cos((345.2533 +  3.0 * mv  -  4.0 * me )*dtor) + \
        1.0 * cos((318.15   +  3.0 * mv  -  5.0 * me )*dtor)
    l = l + vencorr
    
##  Allow for the Mars perturbations using the mean anomaly of Mars MM
    mm = 319.529425  +  ( 19139.858500 * t) % 360.0
    marscorr = 2.0 * cos((343.8883 -  2.0 * mm  +  2.0 * me)*dtor ) + \
        1.8 * cos((200.4017 -  2.0 * mm  + me) * dtor)
    l = l + marscorr

## Allow for the Jupiter perturbations using the mean anomaly of
## Jupiter MJ
    mj = 225.328328  +  ( 3034.6920239 * t) % 360.0
    jupcorr = 7.2 * cos(( 179.5317 - mj + me )*dtor) + \
        2.6 * cos((263.2167 - mj ) *dtor) + \
        2.7 * cos(( 87.1450 - 2.0 * mj + 2.0 * me ) *dtor) + \
        1.6 * cos((109.4933 - 2.0 * mj + me ) *dtor)
    l = l + jupcorr;

## Allow for the Moons perturbations using the mean elongation of
## the Moon from the Sun D
    d = 350.7376814  + ( 445267.11422 * t) % 360.0 
    mooncorr  = 6.5 * sin(d*dtor);
    l = l + mooncorr;
    
## Allow for long period terms
    longterm  = 6.4 * sin(( 231.19  +  20.20 * t )*dtor)
    l  =    l + longterm
    l  =  ( l + 2592000.0) % 1296000.0 
    longmed = l/3600.0
    
## Allow for Aberration
    l  =  l - 20.5;
    
## Allow for Nutation using the longitude of the Moons mean node OMEGA
    omega = 259.183275 - ( 1934.142008 * t ) % 360.0 
    l  =  l - 17.2 * sin(omega*dtor)

## Form the True Obliquity
    oblt  = 23.452294 - 0.0130125*t + (9.2*cos(omega*dtor))/3600.0;

## Form Right Ascension and Declination
    
    l = l/3600.0;
    ra  = atan2( sin(l*dtor) * cos(oblt*dtor) , cos(l*dtor) );
    
    while ((ra < 0) or ( ra > (2*pi))):
        if (ra < 0):
            ra += (2*pi)
        if (ra > (2*pi)):
            ra -= (2*pi)

    dec = asin(sin(l*dtor) * sin(oblt*dtor));
            
    return ra/dtor, dec/dtor 

