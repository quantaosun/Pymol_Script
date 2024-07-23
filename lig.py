#############################################################
#############################################################
#############################################################
## Written by https://github.com/quantaosun/Pymol_Script  ###
#############################################################
#############################################################
#                                                           #
#  This workflow utilizes Python in PyMOL to allow you to   #
#  create a nice image for any protein-ligand system.       #
#                                                           #
#               This file is named lig.py                   #
#  Please feel free to use it. It is for anyone.            #
#############################################################
#############################################################
##############                USAGE              ############
#############################################################
#############################################################
#                                                           #
#                       STEP 1                              #
#                                                           #
#  Open PyMOL, load/fetch your protein-ligand structure.    #
#  It is recommended to remove all other factors like water #
#  and ions, otherwise they will be considered later in     #
#  hydrogen bond interaction generation.                    #
#  Use your mouse, File > Run Script > select this lig.py   #
#                                                           #
#############################################################
#############################################################
#                                                           #
#                       STEP 2                              #
#                                                           #
#  Check what your ligand name is.                          #
#                                                           #
#  Confirm your ligand name, for example, is ABC.           #
#  Go to the PyMOL command line.                            #
#  Type exactly:                                            #
#                                                           #
#                   lig ABC                                 #
#                                                           #
#############################################################
#############################################################
#                                                           #
#                         DONE                              #
#                                                           #
#############################################################
#############################################################
#                                                           #
#  This script can handle most tested structures, but be    #
#  aware:                                                   #
#                                                           #
#  This relies on PyMOL's h_add function to estimate the    #
#  hydrogen positions, which might be slightly different    #
#  from third-party software. Also, please take the         #
#  hydrogen bond interactions with a grain of salt. It may  #
#  miss important interactions and add false ones.          #
#  Hydrophobic interactions are not supported.              #
#                                                           #
#############################################################
########## Note: There are two `lig` keywords in this script: 
### one is used internally by PyMOL, while the other one is 
### defined as a Python function that can use any other name. 
### Here, `lig` is used for descriptive purposes to make the 
### script more intuitive for users in PyMOL.
#############################################################
from pymol import cmd

def lig(ligand):
    # Select the ligand and its surroundings
    #cmd.remove("sol")
    cmd.hide("(hydro)")
    cmd.select("ligand", f"resn {ligand}")
    cmd.select("res", "byres ligand around 5")
    # This distance was set to 5 angstroms
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
    # This section is turned off for simplicity. You can always try
    # to include it as part of automation, but it may take some extra work.
    #####################################################################
    # Generate pseudo atoms for hydrophobic interaction
    # Uncomment and modify the following lines as needed for your specific sites
    # cmd.select("pi_center", "/tmp//A/PHE`241/CD2 | /tmp//A/PHE`241/CE2 | /tmp//A/PHE`241/CZ | /tmp//A/PHE`241/CE1 | /tmp//A/PHE`241/CD1 | /tmp//A/PHE`49/CG")
    # cmd.pseudoatom("pi_center", "sele")
    # cmd.select("res", "pi_center")
    # cmd.show("sphere", "pi_center")

    # Automation of generating hydrophobic interactions is possible, 
    # but it would require more effort than hydrogen bond interactions. 
    # This was not pursued here.
    #####################################################################
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
    ### This section try to detect whether there is already
    ### H added to the structure, if not, it try to guess H 
    ### positions using h_add.
    if not cmd.count_atoms("res and hydro"):
        cmd.h_add("res")
    if not cmd.count_atoms("lig and hydro"):
        cmd.h_add("lig")
    
    # Delete non-polar H
    cmd.select("res")
    cmd.hide("(h. and (e. c extend 1))")
    
    ####################################################################
    # If you enable this section, ALL hydrogen bonds will be overwhelmingly displayed.
    ####################################################################
    # Define polar atoms (N and O) with neighboring hydrogens
    # cmd.select("polar_donors", "(res and elem n,o and (neighbor hydro))")
    # cmd.select("polar_acceptors", "(lig and elem o or (elem n and not (neighbor hydro)))")

    # Select hydrogen atoms bonded to polar donors
    # cmd.select("don_hydrogens", "hydro and (neighbor polar_donors)")
    ####################################################################
    # In the next section, four variables have been defined that belong
    # to two pairs. The first pair is those hydrogen bonds with a direction from
    # protein to ligand, while the second pair is vice versa.
    # Please note, the resulting hydrogen bonds might not make sense
    # since these bonds are only based on proximity. You might need to 
    # delete undesired ones. Nevertheless, it is a good quick way to 
    # get an idea of the interactions.
    ####################################################################
    # Define polar donors in the protein and ligand
    cmd.select("polar_donors_res", "(res and elem n,o and (neighbor hydro))")
    cmd.select("polar_donors_lig", "(lig and elem n,o and (neighbor hydro))")
    
    # Define polar acceptors in the protein and ligand
    cmd.select("polar_acceptors_res", "(res and (elem o or (elem n and not (neighbor hydro))))")
    cmd.select("polar_acceptors_lig", "(lig and (elem o or (elem n and not (neighbor hydro))))")
    
    # Select hydrogen atoms bonded to polar donors
    cmd.select("don_hydrogens_res", "hydro and (neighbor polar_donors_res)")
    cmd.select("don_hydrogens_lig", "hydro and (neighbor polar_donors_lig)")
    
    # Show hydrogen bonds between protein donors and ligand acceptors
    cmd.distance("hbonds_res_to_lig", "don_hydrogens_res", "polar_acceptors_lig", 3.2)
    
    # Show hydrogen bonds between ligand donors and protein acceptors
    cmd.distance("hbonds_lig_to_res", "don_hydrogens_lig", "polar_acceptors_res", 3.2)
    #########################################################
    # Show hydrogen bonds between acceptors and donor hydrogens
    # cmd.distance("hbonds", "don_hydrogens", "polar_acceptors", 3.2)
 
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

    #################################################################
    #### This section is for docked poses, but it does no harm to PDB bank structures.
    ### The reason is to fix the H disappear issue with docked poses.
    cmd.show("licorice", "res")
    cmd.show("licorice", "lig")
    #cmd.hide("hydrogens", "res and (elem H and neighbor elem C)")
    cmd.hide("(elem H and neighbor elem C)")
    print("Script execution finished.")

def lig_cmd(arg):
    lig(arg)

cmd.extend("lig", lig_cmd)

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
