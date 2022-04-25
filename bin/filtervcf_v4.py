#! /usr/bin/env python2.7


## modified for not using the MGE removal step
## changed the threshold for SNP from 20 to 5

import sys

in1 = sys.argv[1] ##raw vcf file
out1 = sys.argv[2] ##output prefix
#mge = sys.argv[3] ##"MGE_staph.bed file
#cov = sys.argv[3] ##coverage file
min_dist = sys.argv[3] ##the distance parameter to compare snp at distance
#ref = sys.argv[4] ##reference file


d1 = [base.strip() for base in open(in1).readlines() if not base.startswith("#") and "INDEL" not in base]
#mge_coord = [base.strip() for base in open(mge).readlines()]

def checkPV4(x):
    l2 = []
    for each in x:
        if each.startswith("PV4="):
            l2.append(each.split("=")[1])
    return l2

def checkdp4(x):
    l1 = []
    for char in x:
        if char.startswith("DP="):
            l1.append(char.split("=")[1])
        elif char.startswith("DP4="):
            l1.append(char.split("=")[1])
        elif char.startswith("MQ="):
            l1.append(char.split("=")[1])
    return l1

#def mge_filt(x):
#    """list of the variants called at each position"""
#
#    vmge = {}
#    for each in x:
#        c1 = each.split("\t")
#
#        for char in mge_coord:
#            d1 = char.split("\t")
#            if int(c1[1]) >= int(d1[0]) and int(c1[1]) <= int(d1[1]):
#                vmge[c1[1]] = each
#
#    var1 = {base.split("\t")[1]:base for base in x}
#    mge_rmd = set(var1) - set(vmge)
#    mge_filt = [var1[base] for base in list(mge_rmd)]
#    return mge_filt

def dist_filter(z):
    j = 0
    k = 0
    others = []
    clust = {}
    a1 = []
    z1 = sorted(z)

    for i in range(len(z1)-1):
        if z1[i+1] - z1[i] < int(min_dist):
            a1 += [z1[i], z1[i+1]]
            clust["c"+str(j)] = a1
        else:
            others += [z1[i], z1[i+1]]
            j += 1
            a1 = []

    lclust = []
    for each in clust:
        lclust += clust[each]

    x1 = set(others)
    x2 = set(lclust)

    fsnps = sorted(list( x1 - x2 ))

    return fsnps

Hetvar = []
Homvar = []
failed = []

for each in d1:

    a1 = each.split("\t")
    a2 = a1[7].split(";")
    a3 = checkdp4(a2)
    a4 = a1[9].split(":")[-2]
    a5 = checkPV4(a2)
    dp4 = a3[1].split(",")
    if float(a1[5]) >50 and int(a3[0]) >5 and int(a3[-1]) >30 and int(dp4[2]) >2 and int(dp4[3]) > 2:
        p1 = [a1[0], a1[1], a1[3],a1[4],a1[5], a3[0],a3[-1]]+dp4
        l1 = int(dp4[2]) / (float(dp4[2]) + float(dp4[0]))
        r1 = int(dp4[3]) / (float(dp4[3]) + float(dp4[1]))
        if len(a5) >0:
            PV4 = a5[0].split(",")
            if float(PV4[0]) >0.001 and float(PV4[2]) > 0.001 and float(PV4[3]) > 0.001:
                if l1 < 0.90 and r1 < 0.90:
                    t1 = [a1[0], a1[1], a1[3],a1[4],a1[5], a3[0],a3[-1]]+dp4 + ["HET"]
                    Hetvar.append("\t".join(t1))
                if l1 > 0.80 and r1 > 0.80:
                    t3 = [a1[0], a1[1], a1[3], a1[4], a1[5], a3[0], a3[-1]] + dp4 + ["HOMO"]
                    Homvar.append("\t".join(t3))
            else:
                t5 = [a1[0], a1[1], a1[3], a1[4], a1[5], a3[0], a3[-1]] + dp4 +["-"]
                failed.append("\t".join(t5))
        else:
            if l1 < 0.90 and r1 < 0.90:
                    t1 = [a1[0], a1[1], a1[3],a1[4],a1[5], a3[0],a3[-1]]+dp4 + ["HET"]
                    Hetvar.append("\t".join(t1))
            if l1 > 0.80 and r1 > 0.80:
                    t3 = [a1[0], a1[1], a1[3], a1[4], a1[5], a3[0], a3[-1]] + dp4 + ["HOMO"]
                    Homvar.append("\t".join(t3))

    else:
        t2 = [a1[0], a1[1], a1[3],a1[4],a1[5], a3[0],a3[-1]] + dp4 + ["-"]
        failed.append("\t".join(t2))


#vfilt1 = mge_filt(fvar)

homfilt = {int(base.split("\t")[1]):base for base in Homvar}
hetfilt = {int(base.split("\t")[1]):base for base in Hetvar}
vdistHom = dist_filter(homfilt.keys())
vdistHet = dist_filter(hetfilt.keys())

homfiltered = [homfilt[int(base)] for base in vdistHom]
hetfiltered = [hetfilt[int(base)] for base in vdistHet]



#c1 = open(cov).read().strip().replace(" ","")
n1 = len(hetfiltered)
n2 = len(homfiltered)

#refSeq = ""
#for line in open(ref).readlines():
#    if not line.startswith(">"):
#        refSeq += line.strip()

try:
    st1 = format(float(n1)/n2, ".2f")

except ZeroDivisionError as err:
    print err
    st1 = 0

finally:
    h1 = ["\t".join("Het_SNPs Total_SNPs Proportion".split(" "))]
    h2 = ["\t".join([str(n1), str(n2), str(st1)])]
    stats = h1+h2

header = "Chrom Pos Ref Alt BaseQ Depth MapQ RF RR AF AR TYPE"
#open(out1+"_failed.vcf","w+").writelines("\n".join(["\t".join(header.split(" "))]+sorted(failed, key = lambda x: int(x.split("\t")[1]))))
open(out1+"_"+min_dist+"stats", "w+").writelines("\n".join(stats))
open(out1+"_"+min_dist+"fhom.vcf","w+").writelines("\n".join(["\t".join(header.split(" "))]+sorted(homfiltered, key = lambda x: int(x.split("\t")[1]))))
open(out1+"_"+min_dist+"fhet.vcf","w+").writelines("\n".join(["\t".join(header.split(" "))]+sorted(hetfiltered, key = lambda x: int(x.split("\t")[1]))))


##for hom snp#'TYPE!="snp" || FORMAT/DP<20 || DP4[2]+DP4[3]<4 || DP4[2]<2 || DP4[3]<2 || DP4[2]/(DP4[2]+DP4[0])<0.75 || DP4[3]/(DP4[3]+DP4[1])<0.75 || QUAL<50 || INFO/MQ<30'
##for het snp#~/Programs/bcftools-1.3.1/bcftools filter -e 'TYPE!="snp" || FORMAT/DP<20 || DP4[2]<2 || DP4[3]<2 || DP4[2]/(DP4[2]+DP4[0])>0.90 || DP4[3]/(DP4[3]+DP4[1])>0.90 ||DP4[0]<2||DP4[1]<2|| QUAL<50 ||SP <20|| INFO/MQ<30' -o het2_filtered.vcf Test10A1L5/samtools.vcf
