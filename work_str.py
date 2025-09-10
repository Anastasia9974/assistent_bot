
def form_answer(answ_answ,answ_data):
    vvv = ""
    a = answ_answ
    delit = 0
    for x in range(len(a)):
        if x + 2 < len(a) and (a[x] != '\\' or a[x + 1] != 'r') and delit == 0:
            vvv = vvv + f"{a[x]}"
        elif x + 2 >= len(a) and delit == 0:
            vvv = vvv + f"{a[x]}"
            continue
        elif delit == 0:
            vvv = vvv + f"\n"
            delit = 3
        else:
            delit -= 1
    #
    if answ_data != '0':
        b = answ_data[-3:]
        if b != 'ipg':
            vvv = vvv + f"\n\r"
            vvv = vvv + f"{answ_data}"
    return vvv