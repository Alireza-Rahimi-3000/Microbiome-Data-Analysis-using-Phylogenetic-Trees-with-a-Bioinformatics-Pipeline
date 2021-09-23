from Bio import Entrez, SeqIO, Phylo
import os

#File IO
filename = input("Enter name of input file: ")
#filename = "taxa_names.txt" #input name of your file containing list of species here
file = open(filename, 'r')
speList = file.read().split("\n")
#print(speList[0])
for id in speList:
    if id == "":   #if the code reads an empty line into the list, an error will rise later so we filter them out now
        speList.remove(id)
        
os.mkdir("PhyloTreeDirectory")
#os.chdir("PhyloTreeDirectory") # switch to this command after the code has been run more than once
outfile = open("16Sout.fasta","w")
log = open("PhyloTreeLog.log","w")

for name in speList:
    #name = "E.coli"
    Entrez.email = "delaneyjosauer@gmail.com"
    handle = Entrez.esearch(db="nucleotide", term = '33175[BioProject] OR 33317[BioProject] AND ("' + name +'"[Organism]') #searching genbank via Entrez and looking for only refseq entries
    record = Entrez.read(handle)
    #print(record["IdList"])
    if len(record["IdList"]) > 0: #added this conditional to keep code going if one species doesn't have a 16S entry 
        ID = record["IdList"][0] #choosing the first ID in the list
        speHandle = Entrez.efetch(db="nucleotide",id = ID,rettype = "gb", retmode = 'text') #searching for the specific ID
        speRecord = SeqIO.read(speHandle,"genbank")
        name = name.replace(" ","_") #spaces must be replaced for FastTree further in pipeline
        #print(name)
        outfile.write(">" + name + " 16S sequence" + "\n" + str(speRecord.seq) + "\n")
        log.write("16S Sequence found for: " + name + "; written in 16Sout.txt" + "\n")
    else:
        log.write("No 16S sequence found for " + name + " so it was removed from tree building" + "\n") #let the user know if the code could not find a seq

#BIG thank you to Dr. Wheeler who helped me out on this code!

#creating sequence alignment w/ MUSCLE via command line
os.system("muscle -in 16Sout.fasta -out seqs.afa")
log.write("Multiple Sequence Alignment made called seqs.afa" +"\n")

#creating newick tree using fasttree
os.system("FastTree -gtr -nt < seqs.afa > tree_file")
log.write("Newick tree file made called tree_file" +"\n")

#you can visualize the newick file on a tree viewer online

file = "tree_file"
tree = Phylo.read(file, "newick")
Phylo.draw_ascii(tree)
log.write("Image of phylogenetic tree created" + "\n" + "Thank you for using our Phylogenetic Tree Maker!")

#at the end of the pipeline, you have a multiple sequence alignment, newick file, an image, and a log file that documented everything done
outfile.close()
log.close()
