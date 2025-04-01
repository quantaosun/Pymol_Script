# This script is only meant to run in the PyMol command line
# 1. load you PDB file, say 6I5I.pdb to pymol
# 2. remove all other small molecules except the real ligand
# 3. Identify the name of the ligand is "H3E"
# 4. Put this script in the same folder as your pdb file and rename it to "lig.py"
# 5. Go to pymol command line, run "run lig.py"
# 6. continue run " lig H3E", and you should see the processed state of the structure
# 7. Use "Ray" button from top right of PyMol to save an image.
from pymol import cmd
# define a function for the atom colour and style
def lig(ligand):
# Select the ligand and its surroundings
    cmd.hide("(hydro)")
    cmd.select("ligand", f"resn {ligand}")
    cmd.select("res", "byres ligand around 5")
    # This distance was set to 5 angstroms
    # Set the ligand to a lig object
    cmd.select("lig", f"resn {ligand}")
    cmd.select("all")
    cmd.hide("everything")
    # Show the ligand and surroundings
    cmd.show("sticks", "lig | res")
    cmd.hide("sticks", "h.")
    cmd.zoom("lig | res")
    # Color ligand carbon atoms yellow
    cmd.color("yellow", "lig & name C*")
    # Color surrounding residues' carbon atoms cyan
    cmd.color("cyan", "res & name C*")
    # Set label and font size
    cmd.set("label_size", 28)
    cmd.set("label_font_id", 8)
    cmd.set("label_color", "grey")
    cmd.set("sphere_scale", 0.25)
    cmd.set("sphere_color", "cyan")
    cmd.set("sphere_scale", 0.35)
    cmd.set("sphere_transparency", 0.3)
    cmd.set("sphere_color", "cyan")
    # Detect whether there is hydrogen added to the structure already
    if not cmd.count_atoms("res and hydro"):
        cmd.h_add("res")
    if not cmd.count_atoms("lig and hydro"):
        cmd.h_add("lig")
    # Delete non-polar H
    cmd.select("res")
    cmd.hide("(h. and (e. c extend 1))")
    # Six variables defined
    cmd.select("polar_donors_res", "(res and elem n,o and (neighbor hydro))")
    cmd.select("polar_donors_lig", "(lig and elem n,o and (neighbor hydro))")
    # Polar acceptors in the protein and ligand (Detect O, N)
    cmd.select("polar_acceptors_res", "(res and (elem o or (elem n and not (neighbor hydro))))")
    cmd.select("polar_acceptors_lig", "(lig and (elem o or (elem n and not (neighbor hydro))))")
    # Hydrogen atoms bonded to polar donors (detect H of OH and NH)
    cmd.select("don_hydrogens_res", "hydro and (neighbor polar_donors_res)")
    cmd.select("don_hydrogens_lig", "hydro and (neighbor polar_donors_lig)")
    # Show distance of two types of hydrogen bonds
    cmd.distance("hbonds_res_to_lig", "don_hydrogens_res","polar_acceptors_lig", 3.2)
    # Hydrogen bonds between ligand donors and protein acceptors
    cmd.distance("hbonds_lig_to_res", "don_hydrogens_lig","polar_acceptors_res", 3.2)
    # Define hydrogen bonds style.
    cmd.set("dash_length", 0.3)
    cmd.set("dash_radius", 0.08)
    cmd.set("dash_color", "yellow")
    cmd.set("dash_width", 2.0)
    cmd.set("dash_gap", 0.5)
    # Set background white
    cmd.bg_color("white")
    # Show cartoon
    cmd.show("cartoon")
    cmd.set("cartoon_transparency", 0.3)
    # Prepare to save as PNG and PSE file
    cmd.set("ray_trace_mode", 1)
    cmd.png("binding_pocket.png")
    cmd.save("pre_pymol.pse")
    # Double check with docked structures
    cmd.show("licorice", "res")
    cmd.show("licorice", "lig")
    cmd.hide("(elem H and neighbor elem C)")
    print("Script execution finished.")
# Define parameter (ligand name) input format
def lig_cmd(arg):
    lig(arg)
cmd.extend("lig", lig_cmd)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.exit(1)
    ligand = sys.argv[1]
    lig(ligand)

