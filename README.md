# Pymol_Script

**STEP 1**   Open PyMOL, load/fetch your protein-ligand structure use your mouse, ```File > Run Script > lig.py``` 
 
**STEP 2**     Check what your ligand name is   Confirm your ligand name, for example, is ```ABC```         
 Go to the PyMOL command line type exactly     ```lig ABC``` , and that's it, the pymol should have done the hard work for you.                      

```python
    ####################################################################
    # This script also suport automatic H-bond detection, here is the
    # part of lig.py responsible for H-bond dection and visulisation.
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
```
![image](https://github.com/user-attachments/assets/61104e76-837f-458b-b4f4-d93333ed9458)

(CRYSTAL STRUCTURE OF THE SARS-COV-2 (2019-NCOV) MAIN PROTEASE IN COMPLEX WITH COMPOUND 4, published by Jorgensen, W.L. et al.)
