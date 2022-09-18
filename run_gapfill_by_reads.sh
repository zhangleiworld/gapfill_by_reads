#!/usr/bin/bash
## Author: Lei Zhang (zhangleo1116@163.com)

## file names and paramenters
assembly=  genome.fasta ## the name of genome assembly for gapfilling
reads= read.fasta ## the reads used to gapfill
length= 100000 ## the sequence length of up- and down-stream of the gap  eg. 100000
thread= 30 ## the thread for minimap eg. 30

## step 1, find the gap position in genome.fasta
python gap_position_finder.py ${assembly}
 
## step 2, pick the up- and down-stream sequences of the gaps 
python pick_gap_updown.py ${assembly} ${assembly}.gap.posi $length

## step 3, map the gap sequences to the reference read.fasta
minimap2 -t ${thread} $reads ${assembly}.gap.posi.fasta > reads_align_gap.paf

## step 4, filter the mapping paf results
python filter_maping_paf.py reads_align_gap.paf $length 

## step 5, replace the gaps with the mapping read seqeences
python replace_gap.py $reads ${assembly} reads_align_gap.paf.gtLen.sort.select $length

