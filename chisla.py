a1=('','один','два','три','четыре','пять','шесть','семь','восемь','девять','десять','одинадцать',
'двенадцать','тринадцать','четырнадцать','пятнадцать','шестнадцать','семнадцать',
'восемнадцать','девятнадцать')

a2=('','десять','двадцать','тридцать','сорок','пятьдесят','шестьдесят','семьдесят','восемьдесят','девяносто')


def chis(n: int):
    if n==0: return 'ноль'
    elif n<20: return a1[n]
    else: return a2[n//10]+" "+a1[n%10]

def anti_chis(s: str):
    out = 0
    s = s.strip().split()

    for i in s:
        if i in a2:
            out += a2.index(i)

        elif i in a1:
            out += a1.index(i)
            

    return out