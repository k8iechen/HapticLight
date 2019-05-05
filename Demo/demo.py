import math, pygame, sys, serial
pygame.init()

class LatLong():
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

    @staticmethod
    def latToMeters(a):
        return a.lat * 111111

    @staticmethod
    def longToMeters(a):
        return a.long * 111111 * math.cos(a.lat)

    def toVector(self):
        return Vector(LatLong.latToMeters(self), LatLong.longToMeters(self))

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def distance(a, b):
        dx = b.x - a.x;
        dy = b.y - a.y;
        return math.hypot(dx, dy);

    @staticmethod
    def subtract(a, b):
        dx = b.x - a.x
        dy = b.y - a.y
        return Vector(dx, dy);

    def inInnerRadius(self, dest):
        if (Vector.distance(self, dest) <= 25):
            return True
        return False

    def inOuterRadius(self, dest):
        if (Vector.distance(self, dest) <= 100):
            return True
        return False

    def angle(self, dest):
        dot_product = (self.x * dest.x) + (self.y * dest.y)
        abs_product = math.hypot(self.x, self.y) * math.hypot(dest.x, dest.y)
        return math.acos(dot_product / abs_product)

    def toLatLong(self):
        lat = self.x / 111111
        long = self.y / 111111 / math.cos(lat)
        return LatLong(lat, long)


origin = LatLong(43.6098737, -79.69257379999999)
origin = origin.toVector()
curr_pos = Vector(origin.x, origin.y)
last_pos = Vector(origin.x, origin.y)
intersect_1 = LatLong(43.608064698191, -79.7470028531623)
intersect_1 = intersect_1.toVector()
intersect_2 = LatLong(43.605796695923, -79.82074394492638)
intersect_2 = intersect_2.toVector()
dest = LatLong(43.604419694545996, -79.86319485101482)
dest = dest.toVector()

#print(origin.inInnerRadius(intersect_1))
#print(origin.inOuterRadius(intersect_2))

route_list = [[origin, "r"], [intersect_1, "l"], [intersect_2, "r"], [dest, "f"]]
route_len = len(route_list)
buffer = 0
i = 1

SCREEN = pygame.display.set_mode([1508, 882])
CLOCK = pygame.time.Clock()
MAP = pygame.image.load('map2.png')
img1 = pygame.image.load('blind.png')
img2 = pygame.image.load('happy.png')
img1 = pygame.transform.smoothscale(img1, [45, 45])
img2 = pygame.transform.smoothscale(img2, [90, 90])
ICON = img1
ALLER = pygame.font.Font('Aller_Rg.ttf', 24)
ALLER.set_bold(True)

while True:
    if (i < route_len - 1) and (curr_pos.x != last_pos.x) and (curr_pos.y != last_pos.y):
        next_traj = Vector.subtract(route_list[i + 1][0], route_list[i][0])
        prev_traj = Vector.subtract(route_list[i][0], route_list[i - 1][0])
        curr_traj = Vector.subtract(curr_pos, route_list[i][0])
        print(math.fabs(math.degrees(curr_traj.angle(prev_traj)) - 180))
        if (curr_pos.inOuterRadius(route_list[i][0])):
            print("Int {} reached".format(i))
            if (math.fabs(curr_traj.angle(next_traj)) <= math.pi / 6):
                i += 1

    # Testing Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            key_down = event.key
            if key_down == pygame.K_q:
                if ICON == img1:
                    ICON = img2
                else:
                    ICON = img1

    if (buffer == 2):
        last_pos.x = curr_pos.x
        last_pos.y = last_pos.y
        buffer = 0;
    buffer += 1

    inp = pygame.key.get_pressed()
    if inp[pygame.K_w] or inp[pygame.K_UP]:
        curr_pos.y -= 3
    if inp[pygame.K_a] or inp[pygame.K_LEFT]:
        curr_pos.x -= 3
    if inp[pygame.K_s] or inp[pygame.K_DOWN]:
        curr_pos.y += 3
    if inp[pygame.K_d]or inp[pygame.K_RIGHT]:
        curr_pos.x += 3


    #coords = curr_pos.toLatLong()
    #print("({}, {})\n".format(coords.lat, coords.long))
    #print(i)
    SCREEN.blit(MAP, [0, 0])
    if ICON == img2:
        SCREEN.blit(ICON, [curr_pos.x - 4844560.6766807, curr_pos.y + 8248098.922644861])
    else:
        SCREEN.blit(ICON, [curr_pos.x - 4844530.6766807, curr_pos.y + 8248143.922644861])

    sig = route_list[i - 1][1]
    direction_string = ""
    if (sig == "l"):
        direction_string = "LEFT"
    elif (sig == "r"):
        direction_string = "RIGHT"

    if (curr_pos.inInnerRadius(route_list[i][0])):
        sig += '1'
        direction_string = "SUDDEN " + direction_string
    elif (curr_pos.inOuterRadius(route_list[i][0])):
        sig += '2'
        direction_string += " SOON"
    else:
        direction_string = "STRAIGHT"

    if (curr_pos.inInnerRadius(route_list[route_len - 1][0])):
        direction_string = "DESTINATION REACHED!"

    SCREEN.blit(ALLER.render('Direction: {0}'.format(direction_string), 0, (0, 0, 0)), (10, 10))
    pygame.display.update()
    CLOCK.tick(30)

    #ser1 = serial.Serial('COM3', 9600)
    #ser1.write(sig.encode())




# 8:20 - A
# C:\Users\David\AppData\Local\Programs\Python\Python36\python.exe math.py
