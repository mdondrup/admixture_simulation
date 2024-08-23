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
demography.add_population(
    name="Kveik",
    description="Kveik without admixture",
    initial_size=isize,
)
demography.add_population(
    name="Dom",
    description="Mainline beer/winw ancestor",
    initial_size=isize,
)
demography.add_population(
    name="Beer0",
    description="Lager Ale ancestor",
    initial_size=isize,
)

demography.add_population(
    name="Wine",
    description="Wine domestication",
    initial_size=isize,
)


demography.add_population(
    name="Sake",
    description="Sake domestication",
    initial_size=isize,
)


demography.add_population(
    name="CH0",
    description="Out of China",
    initial_size=isize,
)

demography.add_population(
    name="Wild", description="Wild S.cerevisiae population",
    initial_size=isize
)
demography.add_population(
    name="ANC",
    description="Ancestral equilibrium population",
    initial_size=isize,
)

demography.add_instantaneous_bottleneck(time=100*gy, strength=600*gy, population="Sake")
demography.add_instantaneous_bottleneck(time=200*gy, strength=200*gy, population="Lager")
demography.add_population_split(500*gy, derived=["Lager", "Ale"], ancestral="Beer0")
demography.add_admixture(time=600*gy, derived="Kveik", ancestral=["Beer0", "Sake"], proportions=[0.7, 0.3])
#demography.add_population_split(1000*gy, derived=[ "Beer0"], ancestral="Dom")
demography.add_population_split(4000*gy, derived=["Wine", "Beer0"], ancestral="Dom")

demography.add_population_split(6000*gy, derived=["Sake", "Dom"], ancestral="CH0")
demography.add_population_split(13000*gy, derived=["CH0"], ancestral="Wild")       
demography.add_population_split(300000*gy, derived=["Wild"], ancestral="ANC")

print(demography)
tup=list(product(["Wild","Sake", "Wine","Ale", "Lager"],range(1,11)))+list(product(["Kveik"],range(1,11)))
nams=list(map(lambda x: x[0]+"_"+str(x[1]), tup))

ts = msprime.sim_ancestry(
    {"Wild":10, "Sake":10, "Wine":10, "Ale":10, "Lager":10, "Kveik":10},
    sequence_length=12e6,
    demography=demography, random_seed=1234)
print("simulating mutations")
mts = msprime.sim_mutations(ts, rate=rate, random_seed=5678, model=msprime.JC69())
print("Total number of mutations: "+str(mts.num_mutations))


print ("writing VCF file " + snakemake.output[0] )
vcf =  re.sub(".gz$", "", snakemake.output[0])
with open(vcf, 'w') as file:
      mts.write_vcf(file, individual_names=nams, allow_position_zero = True, contig_id="1")
      file.close()  

      
check_call(['gzip', vcf ])      
