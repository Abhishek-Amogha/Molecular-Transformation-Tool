import numpy as np
from scipy.spatial.transform import Rotation
from math import gcd


# Function to read molecule coordinates from an XYZ file
def read_xyz_file(file_path):
    molecule_coordinates = [] # Initialize an empty list to store molecule coordinates

    # Start a loop for handling file-related errors
    while True:
        try:
            with open(file_path, 'r') as file:
                # Read the number of atoms from the first line
                total_atoms = int(file.readline().strip())

                # Ignore the second line
                file.readline()

                # Start reading coordinates from the third line
                while len(molecule_coordinates) < total_atoms:
                    line = file.readline().strip()
                    if line:
                        # Read coordinates until we have read total_atoms lines
                        molecule_coordinates.append(list(map(float, line.split()[1:])))
            break
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            user_input = input("Enter a valid file path or type 'exit' to quit: ")
            if user_input.lower() == 'exit':
                return None  # Or handle differently as needed
            file_path = user_input
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            user_input = input("Use a valid file or type 'exit' to quit: ")
            if user_input.lower() == 'exit':
                return None  # Or handle differently as needed
            file_path = user_input

    return np.array(molecule_coordinates)


# Function to store molecule coordinates in a data dictionary
def store_molecule_data(molecule_data_dict):
    # Start a loop for handling user input errors
    while True:
        try:
            molecule_name = input("Enter the name of the molecule: ")
            input_file_path = input("Enter the path of the XYZ file (type 'exit' to return to the main menu): ")

            if input_file_path.lower() == 'exit' or molecule_name.lower() == 'exit':
                break  # Exit the function if the user wants to go back

            molecule_coordinates = read_xyz_file(input_file_path)
            molecule_data_dict[molecule_name] = molecule_coordinates

            print(f"Coordinates of {molecule_name} read successfully and stored")

            # Print all stored molecules
            for name, coordinates in molecule_data_dict.items():
                print(f"Molecule Name: {name}")
                print("Molecule Coordinates:")
                print(molecule_data_dict[name])

            return molecule_data_dict

        except FileNotFoundError:
            print(f"Error: File not found at path {input_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

    return molecule_data_dict


# Function to write new coordinates to an XYZ file
def write_xyz_file(file_path, new_coordinates):
    # Start a loop for handling file-related errors
    while True:
        try:
            with open(file_path, 'r') as file:
                # Read the lines from the file
                lines = file.readlines()

            # Start from the third line to update the coordinates
            for i in range(2, len(lines)):
                # Split each line into strings
                parts = lines[i].split()

                # If the line contains valid numeric data, replace the coordinates
                if len(parts) == 4:
                    lines[i] = f"{parts[0]} {' '.join([f'{coord:.6f}' for coord in new_coordinates[i-2]])}\n"

            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.writelines(lines)

            print(f"Coordinates updated successfully in {file_path}")
            break  # Exit the loop on successful update

        except FileNotFoundError:
            print(f"Error: File not found at path {file_path}")
            retry = input("Do you want to retry? (yes/no): ").lower()
            if retry != 'yes':
                break  # Exit the loop if the user chooses not to retry
        except Exception as e:
            print(f"An error occurred: {e}")
            retry = input("Do you want to retry? (yes/no): ").lower()
            if retry != 'yes':
                break  # Exit the loop if the user chooses not to retry


# Function to transform planes in a molecule
def transform_planes(molecule_data_dict, num_points=3):
    # 3 points make a plane and more points are unnecessary
    while True:
        try:
            molecule_name = input("Enter the name of the molecule (type 'exit' to return to the main menu): ")

            # Exit the function if the user wants to go back
            if molecule_name.lower() == 'exit':
                break  # Exit the function if the user wants to go back

            if molecule_name in molecule_data_dict:
                molecule = molecule_data_dict[molecule_name]

                def find_plane(point1, point2, point3):
                    p1 = np.array(point1)
                    p2 = np.array(point2)
                    p3 = np.array(point3)

                    v1 = p2 - p1
                    v2 = p3 - p1

                    normal_vector = np.cross(v1, v2)

                    a, b, c = normal_vector
                    d = np.dot(normal_vector, p1)

                    # Find the greatest common divisor (GCD) of a, b, c
                    common_factor = gcd(gcd(int(a), int(b)), int(c))

                    if common_factor == 0:
                        common_factor = 1

                    # Simplify coefficients by dividing by the common factor
                    a /= common_factor
                    b /= common_factor
                    c /= common_factor
                    d /= common_factor
                    return a, b, c, d

                def get_point_input(n):
                    # Start a loop for handling invalid input
                    while True:
                        try:
                            input_line = input(f"Enter space-separated coordinates of the {n}th point (x y z): ")
                            x, y, z = map(float, input_line.split())
                            return x, y, z
                        except ValueError:
                            print("Invalid input. Try again.")

                def transform_points(original_points, original_plane, target_plane):
                    original_normal = np.array([original_plane[:3]])
                    target_normal = np.array([target_plane[:3]])

                    align_vectors = Rotation.align_vectors(target_normal, original_normal)
                    rotation_matrix = align_vectors[0].as_matrix()

                    rotated_points = np.dot(original_points, np.transpose(rotation_matrix))

                    return rotated_points, target_normal

                # Input original plane points
                print(f"Enter {num_points} points for the original plane:")
                original_plane_points = [get_point_input(i + 1) for i in range(num_points)]
                original_plane = find_plane(*original_plane_points[:3])

                # Input target plane points
                print(f"Enter {num_points} points for the target plane:")
                target_plane_points = [get_point_input(i + 1) for i in range(num_points)]
                target_plane = find_plane(*target_plane_points[:3])

                # Transform the points
                rotated_points_result, target_normal = transform_points(molecule, original_plane, target_plane)

                # Ask the user to input one of the points of the target plane
                print("Enter one of the points on target plane once again (this is a part of calculation)")
                p1_target_plane = np.array(get_point_input(1))

                # Calculate the translation vector
                translation_vector = rotated_points_result[0] - p1_target_plane

                transformed_points = rotated_points_result + translation_vector

                target_normal /= np.linalg.norm(target_normal)  # Normalize the translation vector
                target_normal *= 2  # Scale the normalized vector by the desired distance
                # We wanted to keep a distance of 2 Armstrong in the final output

                fully_transformed_molecule = transformed_points - target_normal

                print("Transformed the points successfully!")
                molecule_data_dict[molecule_name] = fully_transformed_molecule
                break  # Exit the loop on successful transformation
            else:
                print(f"Molecule with the name {molecule_name} not found.")

        except Exception as e:
            print(f"An error occurred: {e}")


# Function to translate a molecule along a specified vector by a given distance
def translate_molecule(molecule, translation_vector, distance):
    translation_vector /= np.linalg.norm(translation_vector)  # Normalize the translation vector
    translation_vector *= distance  # Scale the normalized vector by the desired distance

    translated_molecule = molecule + translation_vector
    return translated_molecule


# Function to bring the molecule to the origin using a specified set of coordinates
def bring_the_molecule_to_origin(molecule, origin_coord):
    # Subtract the origin_coord from each atom's coordinates
    return molecule - origin_coord


# Function to rotate a molecule around an axis or vector
def rotate_molecule(molecule, rotation_axis):
    while True:
        try:
            angle_degrees = float(input("Enter the rotation angle in degrees: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numerical value for the rotation angle.")

    rotation_matrix = Rotation.from_rotvec(angle_degrees * np.pi / 180 * rotation_axis).as_matrix()
    rotated_molecule = np.dot(molecule, np.transpose(rotation_matrix))
    return rotated_molecule


# Function to align a molecule to a specified axis
def align_molecule_to_axis(molecule, align_option):
    if align_option == "vector":
        # Align to user-specified initial and target vectors
        print("Input initial axis")
        initial_axis = get_the_axis_to_be_aligned_to()
        print("target axis")
        target_axis = get_the_axis_to_be_aligned_to()
    elif align_option == "bond":
        # Align to a vector constructed from two user-specified atoms
        print("NOTE: check index from labelled atoms")
        atom_index1 = int(input("Enter the index of the first atom: ")) - 1
        atom_index2 = int(input("Enter the index of the second atom: ")) - 1
        initial_axis = molecule[atom_index2] - molecule[atom_index1]
        print("Input target axis")
        target_axis = get_the_axis_to_be_aligned_to()
    else:
        print("Invalid align_option. Use 'vector' or 'bond' next time")
        return molecule

    align_vectors = Rotation.align_vectors(np.array([target_axis]), np.array([initial_axis]))
    rotation_matrix = align_vectors[0].as_matrix()
    molecule_after_alignment = np.dot(molecule, np.transpose(rotation_matrix))

    return molecule_after_alignment


# Function to get the axis to be aligned to
def get_the_axis_to_be_aligned_to():
    while True:
        try:
            print("Enter the axis. e.g., 1 0 0 for x-axis, 0 1 0 for y-axis):")
            # Collect user input for the axis vector
            axis = input("Axis (space-separated vector components): ").split()
            # Convert input components to float
            axis = [float(component) for component in axis]
            print(axis)
            # Check if the user entered three numerical components
            if len(axis) == 3:
                return np.array(axis)
            else:
                print("Invalid input. Please enter three numerical components.")
        except ValueError:
            print("Invalid input. Please enter numerical values for the axis components.")


def print_molecule_coordinates(data_dictionary):
    # Get the name of the molecule from the user
    molecule_name = input("Enter the name of the molecule: ")

    if molecule_name in data_dictionary:
        print("Molecule Coordinates:")
        # Print the coordinates of the specified molecule
        print(data_dictionary[molecule_name])
    else:
        print(f"Molecule with the name {molecule_name} not found.")


molecule_data_dict = {}
while True:
    # Get user action
    user_input = input("Enter your action (type 'help' for options): ").lower()

    if user_input == 'help':
        # Display available options
        print("Options:")
        print("1. print molecule : Prints the coordinates of the molecule")
        print("2. store molecule : Stores the coordinates of a molecule, by reading an xyz file")
        print("3. bring to origin : Brings the molecule to the origin")
        print("4. rotate molecule : Rotate a molecule around an axis or vector")
        print("5. align molecule : Align a molecule to a specified axis")
        print("6. transform planes : Make a plane parallel to a specific plane")
        print("7. translate molecule : Translate a molecule along a specified vector by a given distance")
        print("8. replace input file by output file : Update the input file of a molecule with the stored coordinates")
        print("9. exit - Exit the program")
    elif user_input == 'print molecule' or '1':
        # Print the coordinates of a specified molecule
        print_molecule_coordinates(molecule_data_dict)
    elif user_input == 'store molecule' or '2':
        # Store the coordinates of a molecule by reading an xyz file
        molecule_data_dict = store_molecule_data(molecule_data_dict)
    elif user_input == 'bring to origin' or '3':
        molecule_name = input("Enter the name of the molecule: ")
        print("Enter the coordinates of the molecule, which should be brought to the origin")

        if molecule_name in molecule_data_dict:
            molecule = molecule_data_dict[molecule_name]

            try:
                # Get space-separated vector components from the user
                input_coordinates = input("Enter space-separated coordinates that should be moved to origin (e.g., x y z): ")

                # Split the input string into individual components
                coordinates = input_coordinates.split()

                # Convert components to float and create the origin coordinates
                origin_coord = np.array([float(coord) for coord in coordinates])

            except ValueError:
                print("Invalid input. Please enter space-separated numerical values.")

            # Bring the molecule to the origin
            transformed_molecule = bring_the_molecule_to_origin(molecule, origin_coord)
            print("Molecule brought to the origin")
            molecule_data_dict[molecule_name] = transformed_molecule
        else:
            print(f"Molecule with the name {molecule_name} not found.")
    elif user_input == 'rotate molecule' or '4':
        molecule_name = input("Enter the name of the molecule: ")

        if molecule_name in molecule_data_dict:
            molecule = molecule_data_dict[molecule_name]
            print("axis around which the molecule needs to be rotated")
            # Get the axis to be aligned to
            axis = get_the_axis_to_be_aligned_to()
            # Rotate the molecule around the specified axis
            transformed_molecule = rotate_molecule(molecule, axis)
            print("Rotation complete!")
            molecule_data_dict[molecule_name] = transformed_molecule
        else:
            print(f"Molecule with the name {molecule_name} not found.")
    elif user_input == 'align molecule' or '5':
        molecule_name = input("Enter the name of the molecule: ")

        if molecule_name in molecule_data_dict:
            molecule = molecule_data_dict[molecule_name]

            # Align the molecule to a specified axis
            align_option = input("Enter 'vector' to align to a vector or 'bond' to align to a bond: ").lower()

            aligned_molecule = align_molecule_to_axis(molecule, align_option)
            print("Molecule alignment successful!")
            molecule_data_dict[molecule_name] = aligned_molecule
        else:
            print(f"Molecule with the name {molecule_name} not found.")
    elif user_input == 'transform planes' or '6':
        # Transform a plane to make it parallel to a specific plane
        transform_planes(molecule_data_dict)
    elif user_input == 'replace input file by output file' or '8':
        molecule_name = input("Enter the name of the molecule: ")
        if molecule_name in molecule_data_dict:
            file_path = input("Enter the file path for output: ")
            # Write the updated coordinates to an output file
            write_xyz_file(file_path, molecule_data_dict[molecule_name])
        else:
            print(f"Molecule with the name {molecule_name} not found.")
    elif user_input == 'translate molecule' or '7':
        molecule_name = input("Enter the name of the molecule: ")

        if molecule_name in molecule_data_dict:
            molecule = molecule_data_dict[molecule_name]

            print("Enter a vector for the direction of translation")

            while True:
                try:
                    # Get space-separated vector components from the user
                    input_vector = input("Enter space-separated vector components (e.g., x y z): ")

                    # Check if the user wants to exit
                    if input_vector.lower() == 'exit':
                        print("Exiting the translation process.")
                        translation_vector = None
                        break

                    # Split the input string into individual components
                    components = input_vector.split()

                    # Convert components to float and create the translation vector
                    translation_vector = np.array([float(component) for component in components])
                    break

                except ValueError:
                    print("Invalid input for the translation vector. Please enter space-separated numerical values.")

            distance = float(input("Enter the distance of translation: "))

            # Translate the molecule along the specified vector by a given distance
            translated_molecule = translate_molecule(molecule, translation_vector, distance)
            print("Molecule translated!")
            molecule_data_dict[molecule_name] = translated_molecule
        else:
            print(f"Molecule with the name {molecule_name} not found.")
    elif user_input == 'exit' or '9':
        # Exit the program
        print("Exiting the program.")
        break
    else:
        # Invalid action. Display available options
        print("Invalid action. Type 'help' to see available options.")