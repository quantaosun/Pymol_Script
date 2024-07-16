# Pymol_Script

![image](https://github.com/quantaosun/Pymol_Script/assets/75652473/6ece4655-004e-44ae-979b-fbc2277a10b5)

(CRYSTAL STRUCTURE OF THE SARS-COV-2 (2019-NCOV) MAIN PROTEASE IN COMPLEX WITH COMPOUND 4, published by Jorgensen, W.L. et al.)


This straightforward and robust script equips you to generate protein-ligand interaction images effortlessly. 
You can use this for both docked structures and PDB bank structures. All you need to modify is to 

1. rename your protein-ligand structure to be ```output.pdb``` , note all PDB naturally do not contain any H atoms, so you should either use third-party software to preapre the
   structure to add H, or use the ```h_add``` command of pymol to do so.

3. Change the ligand name ```UNL``` to your ligand name; it has to be a three-letter string.

4. The pseudo atoms section must be customised for any hydrophobic staking or Pi-cation/edge interactions.

Put your renamed ```output.pdb``` and copy this script. Save it as a file with a ```pml``` suffix format. Then, use PyMol open your pdb file, then click ```run script``` and select the pml file.

<img width="713" alt="image" src="https://github.com/quantaosun/Pymol_Script/assets/75652473/c133b172-442e-49a2-98c3-7acc91fa25d2">



```
load output.pdb, tmp
#load Docked1.pdb, docked
#select the surrounding, then set it to an object 
# find 5 angstroms around the ligand
select resn UNL
select res, byres sele around 5
#set the ligand to a lig object
select lig, resn UNL
# Select all to hide
select all
# hide everything
hide
# show the ligand and surroundings
show sticks, lig|res
# hide the H atom on the sticks
hide sticks, h.
# zoon on lig and res, background faded
zoom lig|res
# Color ligand carbon atom yellow
color yellow, lig&name C*
# Color ligand carbon atom yellow
color cyan, res&name C*
# Set label and font size
# note you still have to click "residues" from the L dropdown menu to show the label
set label_size, 28
set label_font_id, 8
set label_color, grey

##The next solution is to display the HYDOPHOBIC interaction (but it will only finish some of the work; mainly, make the pseudostem for you automatically).
# First generate pseudo atoms/ please adjust accordingly
#select /tmp//A/PHE`241/CD2 | /tmp//A/PHE`241/CE2 | /tmp//A/PHE`241/CZ | /tmp//A/PHE`241/CE1 | /tmp//A/PHE`241/CD1 | /tmp//A/PHE`49/CG ##Change to your own site #numbers!
pseudoatom pi_center, sele
select res, pi_center
show sphere, pi_center
set sphere_scale, 0.25
set sphere_color, cyan

# We also define some hydrophobic interaction style
set sphere_scale, 0.35
set sphere_transparency, 0.3
set sphere_color, cyan
# Define some hydrogen bonds. interaction style
set dash_length, 0.3
set dash_radius, 0.08
set dash_gap, 0.3
# set background white
bg_color white
show cartoon
set cartoon_transparency, 0.3
bg_color white
set ray_trace_mode, 1
png binding_pocket.png
save pre_pymol.pse
```
