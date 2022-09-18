#!/usr/bin/env python
## Author: Lei Zhang (zhangleo1116@163.com)

import sys
import re
from Bio import SeqIO

seq=open(sys.argv[1],'r') # fasta
gap=open(sys.argv[1]+'.gap.posi','w') # gap posi

gap.write('ID'+'\t'+'start'+'\t'+'end'+'\t'+'length'+'\n')

for seq_record in SeqIO.parse(seq,'fasta'):
	ID=seq_record.id
	fa=str(seq_record.seq)
	list1=[i.start() for i in re.finditer('N+',fa)]
	list2=[j.end()   for j in re.finditer('N+',fa)]
	for k in range(len(list1)):
		length = str(int(list2[k]) - int(list1[k]))
		gap.write(ID+'\t'+str(list1[k])+'\t'+str(list2[k])+'\t'+length+'\n') 
seq.close()
gap.close()
