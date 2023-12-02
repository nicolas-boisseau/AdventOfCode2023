import os.path

from common.common import download_input_if_not_exists, post_answer, capture, capture_all

download_input_if_not_exists(2023)


def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    total_part1 = 0
    total_part2 = 0
    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        for line in lines:
            game = line.split(":")
            game_id = int(capture(r"Game (\d+)", game[0])[0])
            print(f"Game {game_id}")

            plays = game[1].split(";")
            part1_ko = False
            min_cube_counts = {"red": 0, "blue": 0, "green": 0}
            for play in plays:
                cubes_counts = {"red": 0, "blue": 0, "green": 0}

                jets = capture_all(r"(\d+) (red|blue|green)", play)
                if len(jets) == 0:
                    continue

                if part == 1:
                    for jet in jets:
                        cubes_counts[jet[1]] += int(jet[0])

                    if cubes_counts["red"] > 12 or cubes_counts["blue"] > 14 or cubes_counts["green"] > 13:
                        print(f"Game {game_id} is invalid !")
                        part1_ko = True
                        continue
                else:
                    for jet in jets:
                        if int(jet[0]) > min_cube_counts[jet[1]]:
                            min_cube_counts[jet[1]] = int(jet[0])

            if not part1_ko:
                total_part1 += game_id

            total_part2 += min_cube_counts["red"] * min_cube_counts["blue"] * min_cube_counts["green"]

        if part == 1:
            return total_part1
        else:
            return total_part2


if __name__ == '__main__':

    level = 2
    expectedSampleResult = 2286
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        post_answer(2023, level, result)
        print(f"Part {level} result posted !")
