#!/usr/bin/env python
import msprime
from itertools import product
import re
from subprocess import check_call
isize=snakemake.params.isize
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
    initial_size=isize/2,
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
    name="LiquidPhase",
    description="Liquid phase fermentation ancestor",
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
    initial_size=isize,
)

demography.add_population(
    name="CH0",
    description="Out of China",
    initial_size=isize,
)

demography.add_population(
    name="Wild", description="Wild S.cerevisiae population",
    initial_size=10*isize
)
demography.add_population(
    name="ANC",
    description="Ancestral equilibrium population",
    initial_size=10*isize,
)

#################### Events need to be ordered by time (recent to ancient) ###################################
demography.add_instantaneous_bottleneck(time=100*gy, strength=5000*gy, population="Sake")
demography.add_instantaneous_bottleneck(time=200*gy, strength=500*gy, population="AsianFermentation")
demography.add_population_split(600*gy, derived=["Lager", "Ale"], ancestral="Beer")

demography.add_instantaneous_bottleneck(time=400*gy, strength=50*gy, population="Kveik4")
demography.add_instantaneous_bottleneck(time=600*gy, strength=50*gy, population="Kveik3")
demography.add_instantaneous_bottleneck(time=800*gy, strength=50*gy, population="Kveik2")
demography.add_instantaneous_bottleneck(time=500*gy, strength=100*gy, population="Kveik1")

demography.add_instantaneous_bottleneck(time=750*gy, strength=50*gy, population="Kveik4")
demography.add_instantaneous_bottleneck(time=880*gy, strength=50*gy, population="Kveik3")
demography.add_instantaneous_bottleneck(time=980*gy, strength=50*gy, population="Kveik2")
demography.add_instantaneous_bottleneck(time=1080*gy, strength=100*gy, population="Kveik1")
demography.add_instantaneous_bottleneck(time=800*gy, strength=50*gy, population="Kveik2")
demography.add_instantaneous_bottleneck(time=800*gy, strength=50*gy, population="Kveik3")
demography.add_admixture(time=400*gy, derived="Kveik5", ancestral=["Kveik2", "Kveik3"], proportions=[0.4, 0.6])
demography.add_population_split(800*gy, derived=[ "Kveik3", "Kveik4"], ancestral="Kveik34")
demography.add_instantaneous_bottleneck(time=1200*gy, strength=50*gy, population="Kveik1")
demography.add_instantaneous_bottleneck(time=1200*gy, strength=50*gy, population="Kveik2")
demography.add_population_split(1200*gy, derived=["Kveik1", "Kveik2"], ancestral="Kveik12")
demography.add_instantaneous_bottleneck(time=1200*gy, strength=100*gy, population="Kveik12")
demography.add_instantaneous_bottleneck(time=1500*gy, strength=50*gy, population="Kveik34")
demography.add_population_split(1500*gy, derived=["Kveik12", "Kveik34"], ancestral="KveikAnc")
demography.add_population_split(3000*gy, derived=["KveikAnc", "Beer"], ancestral="LiquidPhase")
#demography.add_instantaneous_bottleneck(time=2000*gy, strength=100*gy, population="AsianFermentation")
#demography.add_instantaneous_bottleneck(time=2000*gy, strength=100*gy, population="Sake")

demography.add_population_split(2000*gy, derived=["AsianFermentation", "Sake"], ancestral="AsiaSakeAnc")
demography.add_population_split(8000*gy, derived=["AsiaSakeAnc", "LiquidPhase"], ancestral="CH0")
demography.add_population_split(10000*gy, derived=["CH0"], ancestral="Wild")       
demography.add_population_split(300000*gy, derived=["Wild"], ancestral="ANC")
demography.sort_events()

print(demography)
# Create sample names for 10 individuals per population, treat Kveik as a single population
tup=list(product(["Wild","AsianFermentation", "Sake","Ale", 
                  "Lager"],range(1,11))) + list(product(["Kveik"],range(1,51)))
nams=list(map(lambda x: x[0]+"_"+str(x[1]), tup)) # e.g. Wild_1, Wild_2, ..., Lager_10

ts = msprime.sim_ancestry(
    {"Wild":10, "AsianFermentation":10, "Sake":10, "Ale":10, 
     "Lager":10, "Kveik1":10, "Kveik2":10, "Kveik3":10, "Kveik4":10, "Kveik5":10},
    sequence_length=12e6, # 12 Mb, ~ size of S. cerevisiae genome
    demography=demography, random_seed=1234)
print("simulating mutations")
mts = msprime.sim_mutations(ts, rate=rate, random_seed=5678, model=msprime.JC69())
print("Total number of mutations: "+str(mts.num_mutations))


print ("writing VCF file " + snakemake.output[0] )
vcf =  re.sub(".gz$", "", snakemake.output[0])
# Write uncompressed VCF first, then bgzip
# contig_id="1" to avoid issues with downstream tools that expect contig names to be numeric
with open(vcf, 'w') as file:
      mts.write_vcf(file, individual_names=nams, allow_position_zero = True, contig_id="1")
      file.close()  

      
check_call(['bgzip', vcf ])      
