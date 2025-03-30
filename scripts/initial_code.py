# filepath: /pdb-web-server/pdb-web-server/scripts/initial_code.py
# Pseudocode for detecting sulfur-mediated chalcogen interactions in a PDB file

# Import necessary libraries
import numpy as np
from Bio.PDB import PDBParser

# Define constants
VDW_S = 1.80  # Van der Waals radius of sulfur (S) in Å
VDW_O = 1.52  # Van der Waals radius of oxygen (O) in Å
VDW_N = 1.55  # Van der Waals radius of nitrogen (N) in Å
DISTANCE_THRESHOLD_SO = VDW_S + VDW_O  # 3.32 Å
DISTANCE_THRESHOLD_SN = VDW_S + VDW_N  # 3.35 Å
ANGLE_THETA_MIN = 115  # Minimum angle θ for Ch-bond
ANGLE_THETA_MAX = 155  # Maximum angle θ for Ch-bond
ANGLE_DELTA_MIN = -50  # Minimum torsion angle δ for Ch-bond
ANGLE_DELTA_MAX = 50   # Maximum torsion angle δ for Ch-bond

# Function to calculate distance between two atoms
def calculate_distance(atom1, atom2):
    return np.linalg.norm(atom1.coord - atom2.coord)

# Function to calculate angle θ between centroid, S, and O/N
def calculate_theta(centroid, sulfur, atom):
    vector1 = sulfur.coord - centroid
    vector2 = atom.coord - sulfur.coord
    cos_theta = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    return np.degrees(np.arccos(cos_theta))

# Function to calculate torsion angle δ
def calculate_delta(atom1, centroid, sulfur, atom2):
    b1 = centroid - atom1.coord
    b2 = sulfur.coord - centroid
    b3 = atom2.coord - sulfur.coord

    b1 /= np.linalg.norm(b1)
    b2 /= np.linalg.norm(b2)
    b3 /= np.linalg.norm(b3)

    n1 = np.cross(b1, b2)
    n2 = np.cross(b2, b3)

    n1 /= np.linalg.norm(n1)
    n2 /= np.linalg.norm(n2)

    cos_delta = np.dot(n1, n2)
    delta = np.degrees(np.arccos(cos_delta))

    if np.dot(np.cross(n1, n2), b2) < 0:
        delta = -delta

    return delta

# Main function to detect Ch-bonds
def detect_chalcogen_bonds(pdb_file):
    parser = PDBParser()
    structure = parser.get_structure('protein', pdb_file)

    ch_bonds = []

    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    if atom.element == 'S':
                        sulfur = atom
                        centroid = calculate_centroid(residue)

                        for other_model in structure:
                            for other_chain in other_model:
                                for other_residue in other_chain:
                                    for other_atom in other_residue:
                                        if other_atom.element in ['O', 'N']:
                                            distance = calculate_distance(sulfur, other_atom)

                                            if (other_atom.element == 'O' and distance <= DISTANCE_THRESHOLD_SO) or \
                                               (other_atom.element == 'N' and distance <= DISTANCE_THRESHOLD_SN):

                                                theta = calculate_theta(centroid, sulfur, other_atom)
                                                delta = calculate_delta(other_atom, centroid, sulfur, other_atom)

                                                if ANGLE_THETA_MIN <= theta <= ANGLE_THETA_MAX and \
                                                   ANGLE_DELTA_MIN <= delta <= ANGLE_DELTA_MAX:

                                                    if not is_intramolecular(sulfur, other_atom):
                                                        ch_bonds.append((sulfur, other_atom, distance, theta, delta))

    if len(ch_bonds) > 0:
        print(f"Chalcogen bonds detected: {len(ch_bonds)}")
        for i, bond in enumerate(ch_bonds):
            sulfur, other_atom, distance, theta, delta = bond
            print(f"Debug: ANGLE_DELTA_MIN={ANGLE_DELTA_MIN}, delta={delta}, ANGLE_DELTA_MAX={ANGLE_DELTA_MAX}")
            if ANGLE_DELTA_MIN <= delta <= ANGLE_DELTA_MAX:
                print(f"Ch-bond {i+1}:")
                print(f"  Sulfur position: {sulfur.coord}")
                print(f"  O/N position: {other_atom.coord}")
                print(f"  Distance: {distance:.2f} Å")
                print(f"  Angle θ: {theta:.2f}°")
                print(f"  Torsion angle δ: {delta:.2f}°")
                print(f"  Residue number: {residue.id[1]}")
                print(f"  Chain ID: {chain.id}")
                print(f"  Amino acid: {residue.resname}")
    else:
        print("No chalcogen bonds detected.")

def calculate_centroid(residue):
    coords = [atom.coord for atom in residue]
    return np.mean(coords, axis=0)

def is_intramolecular(atom1, atom2):
    pass

# Example usage
# pdb_file = "./4l81.pdb"
# detect_chalcogen_bonds(pdb_file)