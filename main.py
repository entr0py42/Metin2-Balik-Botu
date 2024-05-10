import pyautogui, time, ctypes, random, os

UYKU = 0.00  # kontrol etme süresi
ORT_BEKLEME = 2.5  # ortalama balık çekme süresi
HATA_PAYI = 0.00  # hata payı
CONSOLE_CLEAR = 2  # kaç balık çektikten sonra konsol temizleme ayarı
RECAST_TIME = 60  # kaç saniye balık gelmedikten sonra yem değiştirip olta atma süresi
BEKLEME = 3  # hile başladıktan sonra ilk oltayı atma süresi

start_time = time.time()


def detectFish(xs, ys):
    x = pyautogui.locateCenterOnScreen("fishemote.png", confidence=0.9, region=(xs - 50, ys - 70, 100, 140))

    if x is None:
        return False
    else:
        return True


def cal():
    x = pyautogui.locateCenterOnScreen("fishemote.png", confidence=0.9)

    if x == None:
        return None
    else:
        return x


SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def KeyPress(key=0x39):
    time.sleep(0)
    PressKey(key)
    time.sleep(.5)
    ReleaseKey(key)


time.sleep(1)

os.system('cls' if os.name == 'nt' else 'clear')
print("Başlamak için chat'e '(fish)' yaz")
print("########################################")
print("ORTALAMA BEKLEME:", ORT_BEKLEME)
print("HATA PAYI:", HATA_PAYI)
print("YENİDEN ATMA SÜRESİ:", RECAST_TIME)
print("########################################")
clearcounter = 0
last_fish = time.time()

initial = None
while initial is None:
    initial = cal()
print(initial)

print("İlk oltanın atılmasına ", BEKLEME, " saniye beklenecek.")
time.sleep(BEKLEME)
print("Yem tak.")
KeyPress(0x05)
time.sleep(1)
print("Olta salla.")
KeyPress()
last_fish = time.time()

s = time.time()

total_baited = 0

while True:

    if time.time() - last_fish > RECAST_TIME:
        print("Son ", round(time.time() - last_fish, 3), " saniyede balık gelmedi. Yeniden olta atılıyor.")
        print("Yem tak.")
        KeyPress(0x05)
        time.sleep(1)
        print("Olta salla.")
        KeyPress()
        last_fish = time.time()

    if detectFish(initial.x, initial.y):
        randomn = (random.randint(0, int(HATA_PAYI * 2 * 100)) - HATA_PAYI * 100) / 100

        total_baited += 1

        a = time.time() - s

        print("Balık geldi.")
        print((ORT_BEKLEME + randomn - (a + b)), "saniye uyu.")
        time.sleep(ORT_BEKLEME + randomn - (a + b))
        print("Çekiliyor...")
        KeyPress()

        print("3sn uyu")
        time.sleep(3)
        print("yem tak")
        KeyPress(0x05)
        time.sleep(0.5)
        print("olta salla")
        KeyPress()

        last_fish = time.time()
        clearcounter += 1
        if clearcounter > CONSOLE_CLEAR:
            clearcounter = 0
            os.system('cls' if os.name == 'nt' else 'clear')
            hours, rest = divmod(time.time() - start_time, 3600)
            minutes, seconds = divmod(rest, 60)
            print("s2cimehmet gururla sunar.")
            print("Geçen süre:", hours, "saat,", minutes, "dakika")
            print("Oltaya gelen toplam:", total_baited)
            print("########################################")
            print("ORTALAMA BEKLEME:", ORT_BEKLEME)
            print("HATA PAYI:", HATA_PAYI)
            print("YENİDEN ATMA SÜRESİ:", RECAST_TIME)
            print("########################################")

    else:
        time.sleep(UYKU)
        b = time.time() - s

    s = time.time()
