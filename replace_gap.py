#!/usr/bin/env python
## Author: Lei Zhang (zhangleo1116@163.com)
import sys
import re
import os
from Bio import SeqIO
from Bio import Seq

## open the input files
ref=open(sys.argv[1]) ## ref genome longreads 
query=open(sys.argv[2]) ## query gap fasta
pos=open(sys.argv[3]) ## position
length=int(sys.argv[4]) ## up and down-stream

## store long-read seq
dict_pos={}
for line1 in pos:
	list1=line1.strip().split()
	dict_pos[list1[5]]=1
pos.close

## store the fasta info
ref_dict={}
for seq_record in SeqIO.parse(ref,'fasta'):
	ID=seq_record.id
	if ID in dict_pos:
		#print(ID)
		ref_dict[ID]=list(seq_record.seq)
ref.close()

query_dict={}
for seq_record in SeqIO.parse(query,'fasta'):
	query_dict[seq_record.id]=list(seq_record.seq)
query.close()

## replace the target sequence
posi=open(sys.argv[3]) ## open again
align_pos=open(sys.argv[3]+'.info.seq','w') ## output info
for line2 in posi:
	list2=line2.strip().split()
	chrom_query=list2[0].split('-')[0]
	strand=list2[4]
	## gap
	gapleft=int(list2[0].split('-')[1])
	gapright=int(list2[0].split('-')[2])
	gaplenth=abs(gapright-gapleft)
	gapstart=int(list2[2])
	gapend=int(list2[3])
	## ref
	chrom_ref=list2[5]
	ref_start = int(list2[7]) + length- gapstart
	ref_end = int(list2[8]) + length- gapend + gaplenth
	if strand == '+':
		replace=''.join(ref_dict[chrom_ref][ref_start:ref_end])
	else:
		seqence=''.join(ref_dict[chrom_ref][ref_start:ref_end])
		my_seq=Seq.Seq(seqence)
		my_seq=my_seq.reverse_complement()
		replace=str(my_seq)
	## not N or n
	#align_pos.write(chrom_query+'\t'+str(gapleft)+'\t'+str(gapright)+'\t'+chrom_ref+'\t'+str(ref_start)+'\t'+str(ref_end)+'\n')
	#align_pos.write(replace+'\n')
	if ('N' not in replace) and ('n' not in replace) :
		for i in range(gapleft,gapright):
			query_dict[chrom_query][i]=''
		query_dict[chrom_query][gapleft]=replace
		align_pos.write(chrom_query+'\t'+str(gapleft)+'\t'+str(gapright)+'\t'+chrom_ref+'\t'+str(ref_start)+'\t'+str(ref_end)+'\n')
		align_pos.write(replace+'\n')
posi.close()
align_pos.close()

## output the replaced sequence
target=open(sys.argv[2]+'.replace.fasta','w')
for j in query_dict:
	target.write('>'+j+'\n')
	target.write(''.join(query_dict[j])+'\n')
target.close()

