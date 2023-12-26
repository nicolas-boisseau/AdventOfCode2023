import os.path

from common.common import download_input_if_not_exists, post_answer, capture, capture_all, read_input_lines

download_input_if_not_exists(2023)

def extract_hailstones(lines):
    hailstones = []
    for line in lines:
        hailstone_raw, speed_raw = line.split(" @ ")
        x, y, z = map(int, capture_all(r"([\d-]+)", hailstone_raw))
        dx, dy, dz = map(int, capture_all(r"([\d-]+)", speed_raw))
        hailstones.append(((x, y, z), (dx, dy, dz)))
    return hailstones

def is_hailstones_crossing(hailstone_a, hailstone_b):
    # http://zonalandeducation.com/mmts/intersections/intersectionOfTwoLines1/intersectionOfTwoLines1.html
    # https://math.stackexchange.com/questions/28503/how-to-find-intersection-of-two-lines-in-3d

    (x1, y1, z1), (dx1, dy1, dz1) = hailstone_a
    (x2, y2, z2), (dx2, dy2, dz2) = hailstone_b

    # f(x1) = x1 + dx1*t
    # f(y1) = y1 + dy1*t
    # f(z1) = z1 + dz1*t

    # g(x2) = x2 + dx2*t
    # g(y2) = y2 + dy2*t
    # g(z2) = z2 + dz2*t

    # find t such as f(x1) = g(x2) and f(y1) = g(y2) and f(z1) = g(z2)

    # x1 + dx1*t = x2 + dx2*s
    # y1 + dy1*t = y2 + dy2*s
    # z1 + dz1*t = z2 + dz2*s

    # x1 + dx1*t - x2 = dx2*s
    # y1 + dy1*t - y2 = dy2*s
    # z1 + dz1*t - z2 = dz2*s

    # s = (x1 + dx1*t - x2) / dx2
    # s = (y1 + dy1*t - y2) / dy2
    # s = (z1 + dz1*t - z2) / dz2

    # t = (x2 - x1 + dx2*s) / dx1
    # t = (y2 - y1 + dy2*s) / dy1
    # t = (z2 - z1 + dz2*s) / dz1

    # t = (x2 - x1 + dx2 * ((x1 + dx1*t - x2) / dx2 )) / dx1
    # t = (y2 - y1 + dy2 * ((y1 + dy1*t - y2) / dy2 )) / dy1
    # t = (z2 - z1 + dz2 * ((z1 + dz1*t - z2) / dz2 )) / dz1

    if dx1 - dx2 != 0:
        t = (dx2*dx1 - dx2*x2 + dx2*x1 - dx2**2 - y1 + y2) / (dy1 - dx2)
        s = (y1 + dy1*t - y2) / dy2


    x1_inter = x1 + dx1*t
    y1_inter = y1 + dy1*t
    z1_inter = z1 + dz1*t

    x2_inter = x2 + dx2*s
    y2_inter = y2 + dy2*s
    z2_inter = z2 + dz2*s

    return x1_inter == x2_inter and y1_inter == y2_inter, (x1_inter, y1_inter, z1_inter)
    #return (x1_inter == x2_inter and y1_inter == y2_inter and z1_inter == z2_inter), (x1_inter, y1_inter, z1_inter)



# f(x) = x0 + dx*t
# f(y) = y0 + dy*t
# f(z) = z0 + dz*t

# g(x) = x1 + dx1*t
# g(y) = y1 + dy1*t
# g(z) = z1 + dz1*t

def part1(lines):
    hailstones = extract_hailstones(lines)

    total = 0
    for i in range(len(hailstones)):
        for j in range(i+1, len(hailstones)):
            if i == j:
                continue
            is_crossing, pos = is_hailstones_crossing(hailstones[i], hailstones[j])
            if is_crossing:
                print(f"{i} and {j} are crossing at {pos}")
                total += 1
    return total



def part2(lines):
    return 4


if __name__ == '__main__':

    part = 1
    expectedSampleResult = -1

    part_func = part1 if part == 1 else part2
    if part_func(read_input_lines("sample.txt")) == expectedSampleResult:
        print(f"Sample for part {part} OK")

        result = part_func(read_input_lines("input.txt"))
        print(f"Input result for part {part} is {result}")

        post_answer(2023, part, result)
        print(f"Part {part} result posted !")
