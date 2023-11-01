# Example pipeline for point cloud data (PCD) manipulation
Using Open3D, the PCD can be downsampled, outliers removed, normals estimated, and mesh created.
Definition and colorization of individual objects is done manually, but ultimately this should be automated.

**Table of Contents**
1. [Directories](#dirs)
2. [Notebooks](#books)
3. [Download and Usage](#usage)
   
### Raw data, no objects defined
<img src="images/monroe_raw.png" width=500/>

### Final scene loaded and visualized as single .ply file
<img src="images/monroe_final.png" width=500/>

## Directories <a name="dirs"></a>
- Data : contains point cloud data in a `.csv`.
- Images : contains screenshots of example outputs.
- Objects : contains predefined objects from the Monroe Hall outdoor scene.

## Notebooks <a name="books"></a>
- `example_pipeline.ipynb` : example pipeline usage for manipulating point cloud data.
- `example_visual.ipynb` : example of loading and visualizing a previously colorized scene.

## Usage <a name="usage"></a>
1. After downloading/cloning the repo, ensure current directory: `cd colorized_proof_of_concept`.
2. run `chmod +x create_conda_env.sh` to create the environemnt.
3. Open the notebook in VS Code or Jupyter and test the example notebooks.