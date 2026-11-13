"""Decorative Discord glyphs. These are not replacements for brand marks."""
from html import escape

def glyph(name, accent='#56B7FF', ink='#FFFFFF'):
    def path(d, color=ink, width=5, fill='none'):
        return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'
    def line(x1,y1,x2,y2,color=ink,width=5):
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
    def circle(cx,cy,r,color=ink,fill='none',width=5):
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="{width}"/>'
    def rect(x,y,w,h,rx=4,color=ink,fill='none',width=5):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{color}" stroke-width="{width}"/>'
    check=path('M15 33 26 44 50 19',accent,6)
    bolt=path('M35 5 13 35 29 35 25 59 51 25 35 25Z',accent,3,accent)
    star=path('M32 5 39 23 58 24 43 37 48 57 32 46 16 57 21 37 6 24 25 23Z',accent,3,'none')
    chart=line(9,9,9,54)+line(9,54,57,54)+path('M15 43 27 32 36 38 53 17',accent)+path('M42 17H53V28',accent)
    trophy=path('M19 8H45V25Q45 40 32 42Q19 40 19 25Z',ink,5)+path('M19 12H8V20Q8 30 21 29M45 12H56V20Q56 30 43 29',accent,4)+line(32,43,32,54)+line(20,57,44,57)
    shield=path('M32 5 53 13V31Q51 48 32 59Q13 48 11 31V13Z')
    people=circle(20,17,8)+circle(46,17,8,accent)+path('M5 54V46Q5 33 20 33Q32 33 34 45V54')+path('M37 35Q60 31 60 48V54',accent)
    search=circle(27,26,18)+line(40,40,58,58,accent,7)
    report=path('M15 5H40L51 16V58H15Z')+path('M40 5V17H51',accent,4)+line(24,29,42,29,accent,4)+line(24,39,42,39,ink,4)+line(24,49,36,49,ink,4)
    signal=line(10,54,10,44,accent,8)+line(25,54,25,34,accent,8)+line(40,54,40,23,ink,8)+line(55,54,55,10,ink,8)
    eye=path('M3 32Q32 4 61 32Q32 60 3 32Z')+circle(32,32,10,accent)
    network=line(32,13,11,48,accent,4)+line(32,13,53,48,accent,4)+line(11,48,53,48,accent,4)+circle(32,12,8,ink,'#122030')+circle(11,49,8,ink,'#122030')+circle(53,49,8,ink,'#122030')
    candle=line(15,5,15,55,ink,3)+rect(9,18,12,23,2,accent,accent,2)+line(34,13,34,59,ink,3)+rect(28,31,12,18,2,ink,'none',3)+line(53,2,53,46,ink,3)+rect(47,9,12,22,2,accent,accent,2)
    rocket=path('M19 39Q17 15 48 5Q61 37 38 46Z')+path('M22 22 10 27 6 43 19 39M43 30 53 42 49 57 38 46',accent,4)+circle(40,20,6,accent,width=3)+path('M22 47 12 58M29 51 23 60',accent,4)
    cube=path('M32 5 56 18V46L32 59 8 46V18Z')+path('M8 18 32 33 56 18M32 33V59',accent,4)
    heart=path('M32 56 7 31Q-1 13 13 8Q26 3 32 17Q39 3 51 8Q65 13 57 31Z',accent,4,accent)
    bull=path('M15 24Q2 19 5 7L17 14M49 24Q62 19 59 7L47 14',accent,5)+path('M16 19Q32 9 48 19L46 44Q42 57 32 58Q22 57 18 44Z')+path('M22 29 26 31M42 29 38 31',accent,4)+path('M23 44Q32 38 41 44V49H23Z',accent,3)
    bear=circle(15,13,8,accent)+circle(49,13,8,accent)+path('M12 24Q12 10 32 10Q52 10 52 24V39Q50 58 32 58Q14 58 12 39Z')+circle(23,30,2,accent,accent,1)+circle(41,30,2,accent,accent,1)+path('M22 42Q32 34 42 42Q42 52 32 53Q22 52 22 42Z',accent,3)+path('M27 42H37L32 47Z',accent,2,accent)
    swords=path('M9 7 39 35 34 40 6 11Z',accent,3)+path('M55 7 25 35 30 40 58 11Z')+line(20,37,35,52,ink,5)+line(43,37,28,52,accent,5)+line(27,45,16,57,ink,6)+line(37,45,48,57,accent,6)
    nodes=circle(32,32,10,accent)+line(32,22,32,6)+line(23,38,9,50)+line(41,38,55,50)+circle(32,6,4,ink,ink,2)+circle(7,52,4,ink,ink,2)+circle(57,52,4,ink,ink,2)
    if name=='node': return nodes
    if name in ('validated','approval','verified'): return shield+check
    if name=='block': return cube
    if name=='linked': return path('M27 19 35 11Q45 1 55 11Q65 21 55 31L43 43Q32 53 22 42',ink,6)+path('M37 45 29 53Q19 63 9 53Q-1 43 9 33L21 21Q32 11 42 22',accent,6)
    if name=='build': return path('M36 9Q49 1 58 11L46 23 41 18 30 29 35 34 23 46 17 40 7 51 13 57 24 47',accent,5)+path('M39 35 55 51Q61 58 54 60Q51 61 47 57L32 42')
    if name=='sync': return path('M52 25Q47 5 27 8Q12 10 8 24M8 24V11M8 24H21',accent)+path('M12 40Q17 60 37 57Q52 55 56 41M56 41V54M56 41H43')
    if name=='launch': return rocket
    if name=='secure': return shield+rect(23,29,18,15,3,accent,accent,2)+path('M25 28V22Q32 10 39 22V28',accent,4)
    if name=='vote': return rect(8,30,48,29,5)+path('M22 31V8H46V31',accent,4)+path('M28 18 32 22 40 13',accent,3)+line(19,39,45,39,ink,4)
    if name=='signal': return signal
    if name=='foundation': return path('M6 24 32 8 58 24Z',accent,4)+line(10,56,54,56)+line(16,30,16,48)+line(32,30,32,48)+line(48,30,48,48)
    if name=='connect': return network
    if name=='grant': return path('M5 41 16 34 29 35Q38 35 38 42H25M38 42 53 31Q61 29 60 36L44 53H17L5 58')+circle(39,15,11,accent)+path('M34 15H44M39 10V20',accent,3)
    if name=='milestone': return path('M14 59V6M15 7H51L43 18 51 29H15',accent)+path('M25 44 32 51 44 37',ink,5)
    if name=='governance': return path('M9 58H55M16 48H48M32 16V47M10 17H54',ink)+circle(32,10,5,accent)+path('M13 19 4 36Q13 45 22 36ZM51 19 42 36Q51 45 60 36Z',accent,4)
    if name=='community': return people
    if name=='roadmap': return path('M10 54H25Q36 54 36 42V24Q36 12 49 12H57',ink,5)+circle(10,54,5,accent,accent,2)+circle(36,33,5,accent,accent,2)+path('M48 5 58 12 48 20',accent,4)
    if name=='announce': return path('M8 26H23L51 12V49L23 37H8Z')+path('M18 38 21 56H33L28 40',accent,4)+line(58,24,62,21,accent,3)+line(58,37,62,40,accent,3)
    if name=='impact': return heart
    if name=='crash': return line(8,7,8,56)+line(8,56,59,56)+path('M16 17 29 31 39 25 55 46M44 46H55V35',accent,6)
    if name=='bear': return bear
    if name=='flat': return line(6,33,58,33,accent,7)+line(12,12,12,16,ink,3)+line(32,12,32,16,ink,3)+line(52,12,52,16,ink,3)+line(12,50,12,54,ink,3)+line(32,50,32,54,ink,3)+line(52,50,52,54,ink,3)
    if name=='bull': return bull
    if name=='moon': return path('M49 8Q21 11 27 34Q32 51 53 46Q43 65 22 55Q2 46 8 25Q14 4 35 5',ink,5)+path('M48 20V30M43 25H53',accent,3)
    if name=='analysis': return candle
    if name=='resolve': return circle(32,32,25,ink)+check
    if name=='volatility': return path('M5 34H14L22 11 31 54 41 20 49 34H59',accent,5)
    if name=='momentum': return path('M6 50 29 26 40 35 59 10M45 10H59V24',accent,6)+line(7,16,17,16,ink,4)+line(7,27,12,27,ink,4)
    if name=='target': return circle(30,34,23)+circle(30,34,12,accent, width=4)+path('M30 34 56 8M45 8H56V19',accent,5)
    if name=='battle': return swords
    if name=='victory': return trophy
    if name=='strategy': return rect(5,5,15,15,2,ink)+rect(44,44,15,15,2,accent)+path('M14 28V50H32M32 50 26 44M32 50 26 56M32 12H53V33M53 33 47 27M53 33 59 27',accent,4)+circle(14,50,3,ink,ink,1)
    if name=='energy': return bolt
    if name=='reward': return path('M13 7H25L32 20 39 7H51L40 28H24Z',ink,4)+circle(32,41,17,accent)+path('M32 31 35 38 43 39 37 44 39 51 32 47 25 51 27 44 21 39 29 38Z',ink,2,ink)
    if name=='defend': return shield+path('M24 26V39M40 26V39M24 32H40',accent,5)
    if name=='defeat': return path('M8 21Q8 7 32 7Q56 7 56 21V40L45 47V57H19V47L8 40Z')+path('M18 25 25 32M25 25 18 32M39 25 46 32M46 25 39 32',accent,4)+line(25,48,25,57,accent,3)+line(33,48,33,57,accent,3)+line(41,48,41,57,accent,3)
    if name=='gg': return path('M17 22H47Q54 22 57 33L61 48Q62 58 53 57L42 46H22L11 57Q2 58 3 48L7 33Q10 22 17 22Z')+path('M17 29V41M11 35H23',accent,4)+circle(45,32,3,accent,accent,2)+circle(51,39,3,accent,accent,2)
    if name=='ready': return path('M9 49V29Q10 7 32 7Q54 7 55 29V49H43V32H21V49Z')+path('M21 26Q32 21 43 26M26 43H38M25 54H39',accent,4)
    if name=='respawn': return path('M54 26Q48 7 30 8Q10 9 8 27M8 27V13M8 27H22',ink,5)+path('M11 40Q18 59 37 56Q53 53 56 40',ink,5)+path('M32 23V43M22 33H42',accent,6)
    if name=='chart': return chart
    if name=='search': return search
    if name=='report': return report
    if name=='status': return circle(32,32,24,ink)+circle(32,32,10,accent,accent,2)+path('M32 1V8M32 56V63M1 32H8M56 32H63',accent,3)
    if name=='filter': return path('M5 9H59L39 33V54L25 60V33Z')+line(18,20,45,20,accent,4)
    if name=='compare': return line(6,56,59,56)+rect(12,26,13,23,2,ink,ink,2)+rect(39,10,13,39,2,accent,accent,2)
    if name=='insight': return path('M20 42Q9 25 20 13Q32 2 44 13Q55 25 44 42L40 48H24Z')+line(25,56,39,56,accent,5)+path('M32 33V45M25 28 32 35 39 28',accent,4)
    if name=='alert': return path('M32 6 59 54H5Z',accent,5)+line(32,23,32,36,ink,6)+circle(32,45,2,ink,ink,2)
    raise KeyError(name)
