# Molecular Transformation Tool

The Molecular Transformation Tool is a Python script that allows users to perform various operations on molecular data, primarily stored in XYZ file format. The tool provides functionalities like storing molecule coordinates, bringing molecules to the origin, rotating molecules, aligning molecules to specific axes, transforming planes, translating molecules, and updating input files with transformed coordinates. With a user-friendly command-line interface, it allows users to perform various transformations and operations on molecules, making it a valuable resource for researchers and professionals working with molecular visualization software.

## Getting Started
### Prerequisites

Make sure you have Python installed on your system. The script uses the following libraries:

1) NumPy
2) SciPy (specifically scipy.spatial.transform.Rotation)

Install the required libraries using:

    pip install numpy 
    pip install scipy

Usage
1) Clone the repository:

          git clone https://github.com/your-username/molecular-transformation-tool.git

2) Navigate to the project directory:

        cd molecular-transformation-tool

3) Run the script:

       python molecular_transformation_tool.py


## Features

### Print Molecule Coordinates
View the coordinates of a molecule stored in the program.

### Store Molecule
Read an XYZ file and store its coordinates for future transformations.

### Bring to Origin
Move a molecule or a subset of its atoms to the origin.

### Rotate Molecule
Rotate a molecule around a specified axis or vector.

### Align Molecule
Align a molecule to a user-specified axis or vector.

### Transform Planes
Make a plane parallel to a specific plane by transforming the molecule.

### Translate Molecule
Translate a molecule along a specified vector by a given distance.

### Replace Input File by Output File
Update the input file of a molecule with the stored coordinates.




## Example Usage

      Enter your action (type 'help' for options): store molecule
      Enter the name of the molecule: water
      Enter the path of the XYZ file (type 'exit' to return to the main menu): /path/to/water.xyz
      Coordinates of water read successfully and stored

      Enter your action (type 'help' for options): transform planes
      Enter the name of the molecule (type 'exit' to return to the main menu): water
      Enter 3 points for the original plane:
      Enter space-separated coordinates of the 1st point (x y z): 0 0 0
      Enter space-separated coordinates of the 2nd point (x y z): 1 0 0
      Enter space-separated coordinates of the 3rd point (x y z): 0 1 0
      Enter 3 points for the target plane:
      Enter space-separated coordinates of the 1st point (x y z): 0 0 0
      Enter space-separated coordinates of the 2nd point (x y z): 1 0 0
      Enter space-separated coordinates of the 3rd point (x y z): 0 0 1
      Enter one of the points on the target plane once again (this is a part of calculation):
      Enter space-separated coordinates of the 1st point (x y z): 0 0 0
      Translation vector: [0. 0. 1.]
      Transformed the points successfully!

Note: The program guides the user through each operation, ensuring ease of use.

## Probable Applications

### Molecular Optimization for Reactions:
Researchers can use the tool to optimize molecular configurations for reactions. By aligning and transforming molecules, users can simulate various reaction intermediates and study the impact on molecular structures.

### Conformational Analysis:
The tool facilitates the exploration of different conformations of molecules. Researchers can rotate, align, and translate molecules to analyze their conformational flexibility and identify stable configurations.

### Structural Biology Studies:
Structural biologists can leverage the tool to align molecules to specific axes or vectors, aiding in the analysis of molecular structures in the context of biological interactions. This can be particularly useful for studying binding sites and molecular recognition.

### Drug Design and Docking Studies:
In drug design, aligning molecules to specific orientations is crucial for docking studies. Researchers can use the Molecular Transformation Tool to prepare molecules for docking simulations by aligning them to desired orientations.

### Comparative Molecular Visualization:
Users can compare different molecular structures by aligning them and visualizing the transformations. This can be helpful for studying structural similarities and differences between molecules.

### Teaching and Learning Tool:
The program can serve as an educational tool for students studying molecular chemistry or computational chemistry. It provides hands-on experience with molecular manipulation and visualization.

### Automation in Molecular Dynamics Simulations:
The tool can be integrated into workflows for molecular dynamics simulations. Researchers can automate the process of preparing molecular structures for simulations by aligning them to specific planes or orientations.
