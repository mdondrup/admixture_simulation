# Snakemake workflow: `admixture_simulation`


A Snakemake workflow for `running TreeMix on simulated data`

The workflow uses msprime to generate VCF files under different demographic models with and without admixture.
Then runs TreeMix with 100 botstrap replicates, and generates a consensus tree.

## Usage

All dependencies are installed via conda. Models are implemented as one python script per model and placed in the scripts folder.
Bootstrap replicates are run in parallel, one core per replicate. Comment out `shell` lines in onstart:  onerror: ... if not using 
messenging script.

Example usage: `snakemake -c <#cpus> --use-conda` runs all models and subsequent TreeMix runs. 

If you use this workflow in a paper, don't forget to give credits to the authors by citing the URL of this (original) <repo>sitory and its DOI (see above).

# TODO

* Replace `<owner>` and `<repo>` everywhere in the template (also under .github/workflows) with the correct `<repo>` name and owning user or organization.
* Replace `<name>` with the workflow name (can be the same as `<repo>`).
* Replace `<description>` with a description of what the workflow does.
* The workflow will occur in the snakemake-workflow-catalog once it has been made public. Then the link under "Usage" will point to the usage instructions if `<owner>` and `<repo>` were correctly set.
