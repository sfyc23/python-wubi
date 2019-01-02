
from pywubi.utlis import (
    single_seg, combin_seg
)

from pywubi.constants import (
    WUBI_86_DICT,
    RE_HANS
)

def single_wubi(han, heteronym=False):
    if len(han) > 1:
        return conbin_wubi(han)
    num = ord(han)
    if num not in WUBI_86_DICT:
        return han
    pys = WUBI_86_DICT[num].split(',')  # 字的拼音列表
    if not heteronym:
        return pys[0]
    return pys


def conbin_wubi(hans):
    len_han = len(hans)
    if len_han == 1:
        return single_wubi(hans)
    elif len_han == 2:
        s = ''
        s += single_wubi(hans[0])[:2]
        s += single_wubi(hans[1])[:2]
        return s
    elif len_han == 3:
        s = ''
        s += single_wubi(hans[0])[0]
        s += single_wubi(hans[1])[0]
        s += single_wubi(hans[2])[:2]
        return s
    elif len_han >= 4:
        s = ''
        s += single_wubi(hans[0])[0]
        s += single_wubi(hans[1])[0]
        s += single_wubi(hans[2])[0]
        s += single_wubi(hans[-1])[0]
        return s


# style=Style.WUBI_86，errors='default'
def wubi(hans, heteronym=False, single=True):
    res = []
    if single:
        han_list = single_seg(hans)
        for han in han_list:
            if RE_HANS.match(han):
                res.append(single_wubi(han, heteronym))
            else:
                res.append(han)
    else:
        han_list = combin_seg(hans)
        for han in han_list:
            if RE_HANS.match(han):
                res.append(conbin_wubi(han))
            else:
                res.append(han)
    return res


# if __name__ == '__main__':
#     hans = '希望s。b好'
#     ret = wubi(hans)
#     print(ret)
