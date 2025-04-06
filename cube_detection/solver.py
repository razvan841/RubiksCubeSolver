import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
import time


# verifyta_path = "\\Users\\dirkw\\Documents\\TCS\\MOD10\\uppaal-4.1.24\\bin-Windows\\verifyta.exe"
verifyta_path = "C:\\Users\\rstef\\uppaal-4.1.24\\bin-Windows\\verifyta.exe"
# solve_path = "C:\\Users\\dirkw\\Documents\\TCS\\MOD10\\uppaal-4.1.24\\project\\cube_project\\"
solve_path = "C:\\Users\\rstef\\Desktop\\Uni\\Module10\\Project\\cps_final_project\\cube_detection\\"

solve_for_command = "part_solve"
solve_for_opening = "part_solve-1.xtr"
command_settings = "-f " + solve_path + solve_for_command + " -t 1"
# model_file = "C:\\Users\\dirkw\\Documents\\TCS\\MOD10\\uppaal-4.1.24\\project\\cube_project\\testcube.xml"
model_file = "C:\\Users\\rstef\\Desktop\\Uni\\Module10\\Project\\cps_final_project\\cube_detection\\testcube.xml"
# query_path = "C:\\Users\\dirkw\\Documents\\TCS\\MOD10\\uppaal-4.1.24\\project\\cube_project\\query_files\\"
query_path = "C:\\Users\\rstef\\Desktop\\Uni\\Module10\\Project\\cps_final_project\\cube_detection\\query_files\\"
move_marker = '999'
cube_marker = '998'
flag_marker = '997'
# solution_file = "C:\\Users\\dirkw\\Documents\\TCS\\MOD10\\uppaal-4.1.24\\project\\cube_project\\solution.txt"
solution_file = "C:\\Users\\rstef\\Desktop\\Uni\\Module10\\Project\\cps_final_project\\cube_solving\\solution.txt"
# final_state_file = "C:\\Users\\dirkw\\Documents\\TCS\\MOD10\\uppaal-4.1.24\\project\\cube_project\\final_state.txt"
final_state_file = "C:\\Users\\rstef\\Desktop\\Uni\\Module10\\Project\\cps_final_project\\cube_solving\\final_state.txt"

# scramble_file = "C:\\Users\\dirkw\\Documents\\TCS\\MOD10\\uppaal-4.1.24\\project\\cube_project\\scramble.txt"

queries = ["white_blue.xtr", "white_red.xtr", "white_green.xtr", "white_cross.xtr",
          "green_orange_corner.xtr", "red_green_corner.xtr", "orange_blue_corner.xtr", "white_face.xtr",
          "green_orange_edge.xtr", "red_green_edge.xtr", "orange_blue_edge.xtr", "second_layer.xtr",
          "yellow_cross.xtr", "yellow_face.xtr", "yellow_corners.xtr" , "fully_solved.xtr"]

INITIAL_FLAGS = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

INITIAL_CUBE_STATE = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
                  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

# Function to build the command
def build_command(query_file):
    command = f"{verifyta_path} {command_settings} {model_file} {query_file}"
    print(command)
    return command

def array_to_string(array):
    # Convert each integer to a string and join them with a comma and a space
    return "{" + ",".join(map(str, array)) + "}"

def read_data(file_path, marker):
    with open(file_path, "r") as file:
        data = file.read().split()
    marker_indices = []
    # Loop through the data to find marker indices
    for i, value in enumerate(data):
        if value == marker:
            marker_indices.append(i)
    last_marker = marker_indices[len(marker_indices) - 1]
    # get the moves
    if marker == move_marker:
        num_moves = int(data[last_marker + 1])
        moves = list(map(int, data[last_marker + 2:last_marker + 2 + num_moves]))
        return moves
    # get the cube state
    if marker == cube_marker:
        cube_state = (list(map(int, data[last_marker + 1:last_marker + 1 + 54])))
        return cube_state
    if marker == flag_marker:
        flags = list(map(int, data[last_marker + 1: last_marker + 1 + 16]))
        return flags

def read_scramble(file_path):
    # Dictionary to store the arrays as lists
    face_arrays = {}

    # Regular expression to match the array pattern
    pattern = r'int (\w+_face)\[9\] = \{([0-9, ]+)\};'

    # Open the file and read its content
    with open(file_path, 'r') as file:
        content = file.read()

        # Find all matches using the regular expression
        matches = re.findall(pattern, content)

        for match in matches:
            # Extract the array name (e.g., 'front_face') and values (e.g., '3,1,0,...')
            face_name, values_str = match
            # Convert the values to a list of integers
            values = list(map(int, values_str.split(',')))
            # Store the list in the dictionary
            face_arrays[face_name] = values
        scramble = face_arrays['front_face']
        scramble.extend(face_arrays['back_face'])
        scramble.extend(face_arrays['right_face'])
        scramble.extend(face_arrays['left_face'])
        scramble.extend(face_arrays['up_face'])
        scramble.extend(face_arrays['down_face'])
    return scramble

def write_moves_to_file(moves, file_path):
    # Convert the list of moves to a string separated by spaces
    moves_str = " ".join(map(str, moves))

    # Open the file in append mode and write the moves
    with open(file_path, "a") as file:
        file.write(moves_str + ' ')

def add_doctype(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.readlines()

    doctype = "<!DOCTYPE nta PUBLIC '-//Uppaal Team//DTD Flat System 1.1//EN' 'http://www.it.uu.se/research/group/darts/uppaal/flat-1_2.dtd'>\n"

    # Insert DOCTYPE after the XML declaration
    if content[0].startswith("<?xml"):
        content.insert(1, doctype)
    else:
        content.insert(0, doctype)

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(content)

def modify_xml(file_path, old_flags, new_flags, old_cube_state, new_cube_state):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Find the 'declaration' element containing the 'turns' definition
    declaration_element = root.find(".//declaration")

    if declaration_element is not None:
        # Get the declaration text and replace 'turns' definition
        declaration_text = declaration_element.text
        # first set the new flags
        updated_declaration = declaration_text.replace(f"int flags[16] = {array_to_string(old_flags)};", f"int flags[16] = {array_to_string(new_flags)};")

        # now set the new faces
        updated_declaration = updated_declaration.replace(f"int front_face[9] = {array_to_string(old_cube_state[0:9])};", f"int front_face[9] = {array_to_string(new_cube_state[0:9])};")
        updated_declaration = updated_declaration.replace(f"int back_face[9] = {array_to_string(old_cube_state[9:18])};", f"int back_face[9] = {array_to_string(new_cube_state[9:18])};")
        updated_declaration = updated_declaration.replace(f"int right_face[9] = {array_to_string(old_cube_state[18:27])};", f"int right_face[9] = {array_to_string(new_cube_state[18:27])};")
        updated_declaration = updated_declaration.replace(f"int left_face[9] = {array_to_string(old_cube_state[27:36])};", f"int left_face[9] = {array_to_string(new_cube_state[27:36])};")
        updated_declaration = updated_declaration.replace(f"int up_face[9] = {array_to_string(old_cube_state[36:45])};", f"int up_face[9] = {array_to_string(new_cube_state[36:45])};")
        updated_declaration = updated_declaration.replace(f"int down_face[9] = {array_to_string(old_cube_state[45:54])};", f"int down_face[9] = {array_to_string(new_cube_state[45:54])};")

        # Update the declaration text
        declaration_element.text = updated_declaration

        # Convert the XML tree to a string
        rough_string = ET.tostring(root, encoding="utf-8")

        # Reformat with minidom for pretty printing and replace empty tags
        parsed = minidom.parseString(rough_string)
        pretty_xml = parsed.toprettyxml(indent="  ")

        # Strip the first XML declaration generated by minidom
        # # Remove the first <?xml ... ?> declaration from the pretty_xml
        pretty_xml = "\n".join(pretty_xml.splitlines()[1:])  # Skip the first line (XML declaration)
         # Remove all extra blank lines between tags
        pretty_xml = "\n".join([line for line in pretty_xml.splitlines() if line.strip()])

        # Ensure empty elements are represented as <tag></tag>
        pretty_xml = pretty_xml.replace("<comment/>", "<comment></comment>")
        pretty_xml = pretty_xml.replace("<formula/>", "<formula></formula>")


        # Add the DOCTYPE
        doctype = "<!DOCTYPE nta PUBLIC '-//Uppaal Team//DTD Flat System 1.1//EN' 'http://www.it.uu.se/research/group/darts/uppaal/flat-1_2.dtd'>"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write('<?xml version="1.0" encoding="utf-8"?>\n')
            file.write(doctype + '\n')
            file.write(pretty_xml.strip())
    else:
        raise ValueError("Declaration element not found in the XML.")


def run(scramble):
    # set up the cube with the scramble and all flags 0
    # also clear the solutions file
    with open(solution_file, 'w') as file:
        pass
    with open(final_state_file, 'w') as file:
        pass
    # scramble = read_scramble(scramble_file)
    modify_xml(model_file, INITIAL_FLAGS, INITIAL_FLAGS, INITIAL_CUBE_STATE, scramble)
    # set these memory arrays of the flags and cube
    old_flags = INITIAL_FLAGS
    old_cube_state = scramble
    solution = []
    # make the current query
    i = 0
    while i < len(queries):
        command_string = build_command(query_path + queries[i])
        # query the model
        os.system(command_string)
        # read the moves, cube state, flags from the model result
        moves = read_data(solve_path + solve_for_opening, move_marker)
        new_cube_state = read_data(solve_path + solve_for_opening, cube_marker)
        new_flags = read_data(solve_path + solve_for_opening, flag_marker)
        # only if we have made progress, ergo when the new flags are different from the old flags, do we update the model
        if new_flags != old_flags:
            # store the moves
            print(moves)
            write_moves_to_file(moves, solution_file)
            solution.extend(moves)
            # i also add a line break between the moveset so that it easier for me to follow
            with open(solution_file, "a") as file:
                file.write('| ')
            # update the model
            modify_xml(model_file, old_flags, new_flags, old_cube_state, new_cube_state)
            # update the old flags and cube state to represent the current model
            old_cube_state = new_cube_state
            old_flags = new_flags
            # we made progress so increment i
            i = i + 1



    with open(final_state_file, 'w') as file:
        file.write(array_to_string(old_cube_state))
    # clean up the cube to all squares = -1 and all flags 0
    modify_xml(model_file, old_flags, INITIAL_FLAGS, old_cube_state, INITIAL_CUBE_STATE)
    return solution


print("###########")
# run([0, 3, 3, 5, 0, 0, 4, 0, 4, 1, 3, 0, 5, 5, 1, 0, 0, 1, 4, 0, 2, 4, 2, 1, 5, 4, 2, 3, 4, 2, 2, 3, 2, 5, 3, 3, 1, 5, 5, 2, 4, 2, 1, 4, 5, 0, 3, 2, 1, 1, 5, 3, 1, 4 ])
