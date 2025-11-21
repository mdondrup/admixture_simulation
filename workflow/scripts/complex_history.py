##!/usr/bin/env python
import msprime
from itertools import product
import re
from subprocess import check_call
isize=snakemake.params.isize # Initial population size
genyear=snakemake.params.genyear
rate=snakemake.params.rate

gy=genyear
demography = msprime.Demography()
demography.add_population(
    name="Lager",
    description= "Modern lager yeasts",
    initial_size=isize,            
)
demography.add_population(
    name="Ale",
    description= "Ale yeasts",
    initial_size=isize,            
)

## Adding multiple Kveik populations to model complex history 
## Identical to complex_history.py but Kveik populations treated as one pooled population
## Kveik1, Kveik2, Kveik3, Kveik4 represent different domestication events
## Sample names will reflect this, but VCF will have only Kveik as population name
## Each Kveik population has its own bottleneck and they all split from a common Kveik ancestor

demography.add_population(
    name="Kveik1",
    description="Kveik 1 group",
    initial_size=isize,
)
demography.add_population(
    name="Kveik2",
    description="Kveik 2 group",
    initial_size=isize,
)   
demography.add_population(
    name="Kveik3",
    description="Kveik 3 group",
    initial_size=isize,
)
demography.add_population(
    name="Kveik4",
    description="Kveik 4 group",
    initial_size=isize,
)  
demography.add_population(
    name="Kveik5",
    description="Kveik 5 internally admixed group",
    initial_size=isize,
) 
demography.add_population(
    name="Kveik34",
    description="Kveik 3 and 4 combined group",
    initial_size=isize,
)
demography.add_population(
    name="Kveik12",
    description="Kveik 1 and 2 combined group",
    initial_size=isize,
)

demography.add_population(
    name="KveikAnc",
    description="Kveik ancestral population",
    initial_size=isize,
)
demography.add_population(
    name="Beer",
    description="Mainline beer ancestor",
    initial_size=isize,
)

demography.add_population(
    name="AsianFermentation",
    description="Asian fermentation population without boottleneck",
    initial_size=isize,
)   

demography.add_population(
    name="Sake",
    description="Sake domestication with strong recent bottleneck",
    initial_size=isize,
)

demography.add_population(
    name="AsiaSakeAnc",
    description="Asia Sake ancestral population",
    initial_size=10*isize,
)
demography.add_population(
    name="SakeAnc",
    description="Sake ancestral population",
    initial_size=isize,
)

demography.add_population(
    name="SakeA",
    description="Sake subpopulation A",
    initial_size=isize,
)
demography.add_population(
    name="SakeB",
    description="Sake subpopulation B",
    initial_size=isize,
)

demography.add_population(
        name="Shadow",
        description="Shadow population to model gene flow",
        initial_size=isize,
    )

demography.add_population(
    name="CH0",
    description="Out of China",
    initial_size=isize,
)

demography.add_population(
    name="Wild", description="Wild S.cerevisiae population",
    initial_size=isize,  
)
demography.add_population(
    name="ANC",
    description="Ancestral equilibrium population",
    initial_size=isize*10,
)

#################### Demographic history (will be ordered) ###################################
demography.add_instantaneous_bottleneck(time=150*gy, strength=500000*gy, population="SakeA")
demography.add_instantaneous_bottleneck(time=150*gy, strength=500000*gy, population="SakeB")

demography.add_population_split(400*gy, derived=["SakeA", "SakeB"], ancestral="SakeAnc")

demography.add_instantaneous_bottleneck(time=3000*gy, strength=100*gy, population="AsianFermentation")

demography.add_population_split(600*gy, derived=["Lager", "Ale"], ancestral="Beer")

#  Adding multiple Kveik populations to model complex history
##
demography.add_instantaneous_bottleneck(time=200*gy, strength=1*gy, population="Kveik1")
demography.add_instantaneous_bottleneck(time=300*gy, strength=1*gy, population="Kveik2")
demography.add_instantaneous_bottleneck(time=500*gy, strength=1*gy, population="Kveik3")
demography.add_instantaneous_bottleneck(time=600*gy, strength=1*gy, population="Kveik4")
demography.add_instantaneous_bottleneck(time=350*gy, strength=1*gy, population="Kveik5")
##

demography.add_admixture(time=400*gy, derived="Kveik5", ancestral=["Kveik2", "Kveik3"], proportions=[0.2, 0.8])
demography.add_population_split(800*gy, derived=[ "Kveik3", "Kveik4"], ancestral="Kveik34")

##
demography.add_instantaneous_bottleneck(time=1000*gy, strength=2000*gy, population="Kveik34")
demography.add_instantaneous_bottleneck(time=1300*gy, strength=2000*gy, population="Kveik12")
##

demography.add_population_split(1200*gy, derived=["Kveik1", "Kveik2"], ancestral="Kveik12")

demography.add_population_split(3000*gy, derived=["Kveik12", "Kveik34"], ancestral="KveikAnc")

demography.set_migration_rate(source="Shadow", dest="KveikAnc", rate=1)

demography.set_migration_rate(source="Shadow", dest="AsiaSakeAnc", rate=1e-2)

demography.add_population_split(3000*gy, derived=["AsianFermentation", "SakeAnc"], ancestral="AsiaSakeAnc")
demography.add_population_split(1500*gy, derived=["Beer"], ancestral="KveikAnc")

demography.add_instantaneous_bottleneck(time=1800*gy, strength=500*gy, population="KveikAnc")

demography.add_instantaneous_bottleneck(time=4000*gy, strength=100*gy, population="KveikAnc")
demography.add_instantaneous_bottleneck(time=4500*gy, strength=100*gy, population="KveikAnc")
demography.add_instantaneous_bottleneck(time=5000*gy, strength=100*gy, population="KveikAnc")

demography.add_population_split(6000*gy, derived=["KveikAnc"], ancestral="AsiaSakeAnc")
###
demography.add_population_split(6000*gy, derived=["Shadow"], ancestral="CH0")

demography.add_population_split(6000*gy, derived=["AsiaSakeAnc"], ancestral="CH0")
demography.add_population_split(10000*gy, derived=["CH0"], ancestral="Wild")       
demography.add_population_split(100000*gy, derived=["Wild"], ancestral="ANC")
demography.sort_events()

print(demography)
#print(demography)

# Create sample names for 10 individuals per population, treat Sake and Kveik as pooled populations
tup=list(product(["Wild","AsianFermentation", "Ale", "Lager", "SakeA", "SakeB",
                  "Kveik1", "Kveik2", "Kveik3", "Kveik4"
                  ],range(1,11))) + list(product(["Kveik5"],range(1,6)))
nams=list(map(lambda x: x[0]+"_"+str(x[1]), tup)) # e.g. Wild_1, Wild_2, ..., Lager_10
print("Sample names: ", nams)
ts = msprime.sim_ancestry(
    {"Wild":10, "AsianFermentation":10,  "Ale":10, "Lager":10,
     "SakeA":10, "SakeB":10, 
     "Kveik1":10, "Kveik2":10, "Kveik3":10, "Kveik4":10, "Kveik5":5},
    sequence_length=12e6, # 12 Mb, ~ size of S. cerevisiae genome
    ploidy=2, # simulate mostly tetraploid genomes
    demography=demography, random_seed=1234)
print("simulating mutations")
mts = msprime.sim_mutations(ts, rate=rate, random_seed=5678, model=msprime.JC69(), discrete_genome=True)
print("Total number of mutations: "+str(mts.num_mutations))


print ("writing VCF file " + snakemake.output[0] )
vcf =  re.sub(".gz$", "", snakemake.output[0])
# Write uncompressed VCF first, then bgzip
# contig_id="1" to avoid issues with downstream tools that expect contig names to be numeric
with open(vcf, 'w') as file:
      mts.write_vcf(file, individual_names=nams, allow_position_zero = True, contig_id="1")
      file.close()  

#SVG(mts.draw_svg())

      
check_call(['bgzip', vcf ])      
print("done")