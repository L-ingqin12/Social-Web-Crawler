import random

"""
对x-zse-96的参数进行加密
"""
h = {
    "zk": [
        1170614578, 1024848638, 1413669199, -343334464, -766094290, -1373058082, -143119608, -297228157, 1933479194,
        -971186181, -406453910, 460404854, -547427574, -1891326262, -1679095901, 2119585428, -2029270069, 2035090028,
        -1521520070, -5587175, -77751101, -2094365853, -1243052806, 1579901135, 1321810770, 456816404, -1391643889,
        -229302305, 330002838, -788960546, 363569021, -1947871109,
    ],
    "zb": [
        20, 223, 245, 7, 248, 2, 194, 209, 87, 6, 227, 253, 240, 128, 222, 91, 237, 9, 125, 157, 230, 93, 252, 205, 90,
        79, 144, 199, 159, 197, 186, 167, 39, 37, 156, 198, 38, 42, 43, 168, 217, 153, 15, 103, 80, 189, 71, 191, 97,
        84, 247, 95, 36, 69, 14, 35, 12, 171, 28, 114, 178, 148, 86, 182, 32, 83, 158, 109, 22, 255, 94, 238, 151, 85,
        77,
        124, 254, 18, 4, 26, 123, 176, 232, 193, 131, 172, 143, 142, 150, 30, 10, 146, 162, 62, 224, 218, 196, 229, 1,
        192, 213, 27, 110, 56, 231, 180, 138, 107, 242, 187, 54, 120, 19, 44, 117, 228, 215, 203, 53, 239, 251, 127, 81,
        11, 133, 96, 204, 132, 41, 115, 73, 55, 249, 147, 102, 48, 122, 145, 106, 118, 74, 190, 29, 16, 174, 5, 177,
        129, 63, 113, 99, 31, 161, 76, 246, 34, 211, 13, 60, 68, 207, 160, 65, 111, 82, 165, 67, 169, 225, 57, 112, 244,
        155, 51, 236, 200, 233, 58, 61, 47, 100, 137, 185, 64, 17, 70, 234, 163, 219, 108, 170, 166, 59, 149, 52, 105,
        24, 212, 78, 173, 45, 0, 116, 226, 119, 136, 206, 135, 175, 195, 25, 92, 121, 208, 126, 139, 3, 75, 141, 21,
        130, 98, 241, 40, 154, 66, 184, 49, 181, 46, 243, 88, 101, 183, 8, 23, 72, 188, 104, 179, 210, 134, 250, 201,
        164, 89, 216, 202, 220, 50, 221, 152, 140, 33, 235, 214,
    ],
}
zk = h['zk']
zb = h['zb']


def i(e, t, n):
    t[n] = 255 & (e >> 24)
    t[n + 1] = 255 & (e >> 16)
    t[n + 2] = 255 & (e >> 8)
    t[n + 3] = 255 & e


def B(e, t):
    return ((255 & e[t]) << 24) | ((255 & e[t + 1]) << 16) | ((255 & e[t + 2]) << 8) | (255 & e[t + 3])


def Q(e, t):
    return ((4294967295 & e) << t) | (e >> (32 - t))


def G(e):
    t = [0] * 4
    n = [0] * 4
    i(e, t, 0)
    n[0] = zb[255 & t[0]]
    n[1] = zb[255 & t[1]]
    n[2] = zb[255 & t[2]]
    n[3] = zb[255 & t[3]]
    r = B(n, 0)
    return r ^ Q(r, 2) ^ Q(r, 10) ^ Q(r, 18) ^ Q(r, 24)


g = {
    'x': lambda e, t: __x(e, t),
    'r': lambda e: __r(e),
}


def __x(e, t):
    n = []
    r = len(e)
    _ = 0
    while r > 0:
        a = [0] * 16
        o = e[16 * _: 16 * (_ + 1)]
        for c in range(16):
            a[c] = o[c] ^ t[c]
        t = g['r'](a)
        n += t
        _ += 1
        r -= 16
    return n


def __r(e):
    t = [0] * 16
    n = [0] * 36
    n[0] = B(e, 0)
    n[1] = B(e, 4)
    n[2] = B(e, 8)
    n[3] = B(e, 12)
    for r in range(32):
        o = G(n[r + 1] ^ n[r + 2] ^ n[r + 3] ^ zk[r])
        n[r + 4] = n[r] ^ o
    i(n[35], t, 0)
    i(n[34], t, 4)
    i(n[33], t, 8)
    i(n[32], t, 12)
    return t


def encode(param):
    salt = '6fpLRqJO8M/c3jnYxFkUVC4ZIG12SiH=5v0mXDazWBTsuw7QetbKdoPyAl+hN9rgE'
    result = ''
    for x in [0, 6, 12, 18]:
        a = param >> x
        b = a & 63
        c = salt[b]
        result += c
    return result


def pre_process(md5Str):
    md5_char_code_at_arr = []
    for _ in range(len(md5Str)):
        md5_char_code_at_arr.append(ord(md5Str[_]))
    md5_char_code_at_arr.insert(0, 0)
    md5_char_code_at_arr.insert(0, int(random.randint(0, 127)))

    for _ in range(15):
        md5_char_code_at_arr.append(14)

    md5_char_code_at_front_arr = md5_char_code_at_arr[:16]
    fix_arr = [48, 53, 57, 48, 53, 51, 102, 55, 100, 49, 53, 101, 48, 49, 100, 55]
    new_md5_char_code_at_arr = []
    for _ in range(len(md5_char_code_at_front_arr)):
        new_md5_char_code_at_arr.append(md5_char_code_at_front_arr[_] ^ fix_arr[_] ^ 42)

    __g_r = g['r'](new_md5_char_code_at_arr)
    md5_char_code_at_back_arr = md5_char_code_at_arr[16:48]
    __g_x = g['x'](md5_char_code_at_back_arr, __g_r)
    return __g_r + __g_x


def encrypt(md5_str):
    processed = pre_process(md5_str)
    current = 0
    result_str = ''
    for _ in range(len(processed)):
        pop = processed[len(processed) - _ - 1]
        i_mod_4 = _ % 4
        i_mod_3 = _ % 3
        a = 8 * i_mod_4
        b = 58 >> a
        c = b & 255
        d = pop ^ c
        e = d << (8 * i_mod_3)
        current |= e
        if i_mod_3 == 2:
            result_str += encode(current)
            current = 0
    return result_str


if __name__ == '__main__':
    import time

    start_time = time.time()
    for _ in range(10000):
        print(encrypt("7aedd7fbc5c3bfd636ddeac76cd82e43"))

    end_time = time.time()

    print("运行时间为：", end_time - start_time, "秒")
