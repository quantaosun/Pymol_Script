#############################################################
#############################################################
#############################################################
## Written by https://github.com/quantaosun/Pymol_Script  ###
#############################################################
#############################################################
#                                                           #
#  This workflow utilizes Python in PyMOL to allow you to   #
#  make a nice image for any protein-ligand system.         #
#                                                           #
#               This file is named as lig.py                #
#  Please feel free to use, it is for anyone.               #
#############################################################
#############################################################
##############                USAGE              ############
#############################################################
#############################################################
#                                                           #
#                       STEP 1                              #
#                                                           #
#  Open PyMOL, load/fetch your protein-ligand structure     #
#  use your mouse, File > Run Script > select this lig.py   #
#                                                           #
#############################################################
#############################################################
#                                                           #
#                       STEP 2                              #
#                                                           #
#  Check what your ligand name is                           #
#                                                           #
#  Confirm your ligand name, for example, is ABC            #
#  Go to the PyMOL command line                             #
#  Type exactly                                             #
#                                                           #
#                   lig('ABC')                              #
#                                                           #
#############################################################
#############################################################
#                                                           #
#                         DONE                              #
#                                                           #
#############################################################
#############################################################
###############               REMINDER        ###############
#############################################################
#                                                           #
#  This script can deal with most tested structures but be  #
#  aware.                                                   #
#                                                           #
#  This relies on PyMOL's h_add function to estimate the    #
#  hydrogen that might be slightly different from a third-  #
#  party software.                                          #
#                                                           #
#############################################################
from pymol import cmd

def lig(ligand):
    # Load the PDB file
    #cmd.load("output.pdb", "tmp")
    # cmd.load("Docked1.pdb", "docked")

    # Select the ligand and its surroundings
    cmd.select("ligand", f"resn {ligand}")
    cmd.select("res", "byres ligand around 5")
    
    # Set the ligand to a lig object
    cmd.select("lig", f"resn {ligand}")
    
    # Select all to hide
    cmd.select("all")
    
    # Hide everything
    cmd.hide("everything")
    
    # Show the ligand and surroundings
    cmd.show("sticks", "lig | res")
    
    # Hide the H atoms on the sticks
    cmd.hide("sticks", "h.")
    
    # Zoom on ligand and surroundings, background faded
    cmd.zoom("lig | res")
    
    # Color ligand carbon atoms yellow
    cmd.color("yellow", "lig & name C*")
    
    # Color surrounding residues' carbon atoms cyan
    cmd.color("cyan", "res & name C*")
    
    # Set label and font size
    cmd.set("label_size", 28)
    cmd.set("label_font_id", 8)
    cmd.set("label_color", "grey")

    # Generate pseudo atoms for hydrophobic interaction
    # Uncomment and modify the following lines as needed for your specific sites
    # cmd.select("pi_center", "/tmp//A/PHE`241/CD2 | /tmp//A/PHE`241/CE2 | /tmp//A/PHE`241/CZ | /tmp//A/PHE`241/CE1 | /tmp//A/PHE`241/CD1 | /tmp//A/PHE`49/CG")
    # cmd.pseudoatom("pi_center", "sele")
    # cmd.select("res", "pi_center")
    # cmd.show("sphere", "pi_center")
    
    cmd.set("sphere_scale", 0.25)
    cmd.set("sphere_color", "cyan")
    
    # Define hydrophobic interaction style
    cmd.set("sphere_scale", 0.35)
    cmd.set("sphere_transparency", 0.3)
    cmd.set("sphere_color", "cyan")
    
    # Define hydrogen bond interaction style
    cmd.set("dash_length", 0.3)
    cmd.set("dash_radius", 0.08)
    cmd.set("dash_gap", 0.3)
    
    # Show the hydrogens
    cmd.h_add("res")
    cmd.h_add("lig")
    
    # Delete non-polar H
    cmd.select("res")
    cmd.hide("(h. and (e. c extend 1))")
    
    # Set background white
    cmd.bg_color("white")
    
    # Show cartoon
    cmd.show("cartoon")
    cmd.set("cartoon_transparency", 0.3)
    
    # Prepare to save as PNG and PSE file
    cmd.set("ray_trace_mode", 1)
    cmd.png("binding_pocket.png")
    cmd.save("pre_pymol.pse")

    print("Script execution finished.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python run_pymol.py LIGAND_NAME")
        sys.exit(1)

    ligand = sys.argv[1]
    lig(ligand)
    
#############################################################
###############                            ##################
#############################################################
#                                                           #
#  "Keep calm and visualize on!"                            #
#                                                           #
#  Your protein-ligand complex thanks you for giving it     #
#  the attention it deserves.                               #
#                                                           #
#############################################################
#############################################################

