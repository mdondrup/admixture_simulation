### An R-script that converts Weir-Cockerham Fst values from VCF tools into a bed file
### In addition does some diagnotic plots. Supposed to run in Snakemake

require(ggplot2)
require(tidyverse)
require(GenomicRanges)

wfst<- read.delim(snakemake@input[['wfst']])

names(wfst) <- tolower(names(wfst))

my_threshold <- snakemake@params[['threshold']]

pdf(file=snakemake@output[['plot']])

plot(density(wfst$weighted_fst, na.rm = T ), main = "Density of mean Windowed-FST")

wfst <- wfst %>% mutate(outlier = ifelse(mean_fst >= my_threshold, "outlier", "background"))
wfst %>% group_by(outlier) %>% tally()


ggplot(wfst, aes(  x=as.integer((bin_start+bin_end)/2), y=mean_fst,colour = outlier, fill=as.factor(chrom))) + geom_point() + labs(x = "Chromosome", y = "windowed Fst") +
facet_grid(~chrom, scales = 'free_x', space = 'free_x', switch = 'x') + 
  theme_classic() + 
  theme(axis.text.x = element_blank(),
        axis.ticks.x = element_blank(),
        panel.margin = unit(0, "lines"))

grfst <- GRanges(seqnames=wfst$chrom, ranges=IRanges(start = wfst$bin_start, end=wfst$bin_end), fst=wfst$mean_fst, outlier=wfst$outlier)[!is.na(wfst$outlier) & wfst$outlier  == "outlier"]

#### using write table instead of rtracklayer to write bed is more flexible
write.table(data.frame(seqnames(grfst), start(grfst), end(grfst), name=grfst$outlier, score=grfst$fst), file=snakemake@output[['bed']], col.names = F, sep="\t", quote=F, row.names = F)

#sum (!is.na(wfst$outlier) & wfst$outlier!="outlier")
dev.off()
