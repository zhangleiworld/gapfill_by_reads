#!/usr/bin/env python
## Author: Lei Zhang (zhangleo1116@163.com)
import sys
import re
import os
from Bio import SeqIO

## open the input files
seq=open(sys.argv[1])    #fasta
pos=open(sys.argv[2])    #posi
length=int(sys.argv[3]) ## up and down-stream

## store the fasta info
seq_dict={}
for seq_record in SeqIO.parse(seq,'fasta'):
	seq_dict[seq_record.id]=str(seq_record.seq)
seq.close()

## output the target sequence
target=open(sys.argv[2]+'.fasta','w')
for line2 in pos:
	if 'ID' not in line2:
		list2=line2.strip().split()
		ID=list2[0]+'-'+list2[1]+'-'+list2[2]
		chrom=list2[0]
		start=int(list2[1]) - length
		end=int(list2[2]) + length
		target.write('>'+ID+'\n')
		target.write(seq_dict[chrom][start:end]+'\n')
pos.close()
target.close()
