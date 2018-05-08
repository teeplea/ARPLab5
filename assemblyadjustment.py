from __future__ import print_function

row_definitions = [
    (7, 1),
    (11, 1),
    (13, 2),
    (15, 7),
    (13, 2),
    (11, 1),
    (7, 1)
]

core_characters = ['A', 'B']
core_character_count = 0
letter_tally = {'A': 1, 'B': 1, 'C': 1}

def main():
    rows = expand_row_definitions()
    row_width_max = max(rows)
    num_rows = len(rows)
    output_line_number = 1
    for i in range(0, num_rows):
        shell_depth = get_shell_depth(rows, i)
        pad = row_width_max - rows[i]
        remaining_counter = rows[i]

        print("%2d " % output_line_number, end='')
        print("%2d" % (1), end='')

        # Pre padding
        for cell in range(0, pad/2):
            print("    ", end='')
            get_core_character()
        # Shell left
        for cell in range(0, shell_depth/2 + shell_depth%2):
            remaining_counter -= 1
            print_letter('C')
            get_core_character()
        # Core
        for cell in range(0, remaining_counter - shell_depth/2):
            print_letter(get_core_character())
        # Shell right
        for cell in range(0, shell_depth/2):
            print_letter('C')
            get_core_character()
        # Post padding
        for cell in range(0, pad/2):
            print("    ", end='')
            get_core_character()
        print("\n", end='')
        output_line_number += 1
    print(" 0  0")

def print_letter(letter):
    global letter_tally
    print(' %s%02d' % (letter, letter_tally[letter]), end='')
    letter_tally[letter] += 1

def get_core_character():
    global core_characters
    global core_character_count
    temp = core_characters[core_character_count % 2]
    core_character_count += 1
    return temp

def find_largest_square(rows):
    max_width_possible = 0
    square_row_index = 0
    for i in range(0,len(rows)):
        width = rows[i]
        # now check if possible
        if width > len(rows) - i:
            break
        try:
            for j in range(i, i + width):
                if rows[j] < width:
                    raise Exception("Nope")
        except:
            break
        max_width_possible = width
        square_row_index = i
    return (max_width_possible, i)

def get_shell_depth(rows, index):
    max_square = find_largest_square(rows)
    num_rows = len(rows)
    corner_rows = [max_square[1], num_rows - max_square[1] - 1]
    if index in [0, len(rows) - 1]:
        return rows[index]
    if (rows[index] - rows[index + 1]) == 4 or \
       (rows[index] - rows[index - 1]) == 4:
        return 6
    if (rows[index] - rows[index + 1]) == 2 or \
       (rows[index] - rows[index - 1]) == 2:
        if index in corner_rows:
            return 2
        else:
            return 4
    else:
        return 2

def expand_row_definitions():
    return sum([[r[0]] * r[1] for r in row_definitions], [])

if __name__ == '__main__':
    main()
