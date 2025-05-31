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

