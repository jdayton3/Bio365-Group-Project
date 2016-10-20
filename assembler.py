import sys
import itertools
import math
sys.setrecursionlimit(10000)


def new_node():
    return {
        'in_nodes': [],
        'out_nodes': []
    }


def add_node(nodes, name):
    if name not in nodes:
        nodes[name] = new_node()

def add_nodes(nodes, head, tail):
    add_node(nodes, head)
    add_node(nodes, tail)
    nodes[head]['out_nodes'].append(tail)
    nodes[tail]['in_nodes'].append(head)

# look at last item in contig - if it's a branching node, we're done, otherwise keep going
def continue_contig(contig):
    end = contig[-1]
    if nodes[end]['branching']:
        return contig[0] + ''.join(i[-1] for i in contig[1:])
    else:
        contig.append(edge_dict[end][0])
        return continue_contig(contig)

# read fasta file
def get_reads(file_name):
    with open(file_name) as file:
        reads = [line.rstrip() for line in file.readlines() if not line.startswith('>')]
    return reads

# get stats about contigs
def get_stats(contigs):
    lengths = [len(c) for c in contigs]
    num_contigs = len(contigs)
    average_length = round(sum(lengths) / float(num_contigs), 2)
    longest = max(lengths)
    return [num_contigs, average_length, longest]


# take file from command line and specify k's here
min_k = 10
max_k = 20
reads = get_reads(sys.argv[1])

# hold stats for contigs generated for each kmer size
stats = {}
for k in range(min_k, max_k + 1):
    nodes = {}
    kmers = []
    kmer_counts = {}
    for read in reads:
        for i in range(len(read)):
            kmer = read[i: i + k]
            if 'N' not in kmer and len(kmer) == k:
                kmers.append(kmer)
                if kmer not in kmer_counts:
                    kmer_counts[kmer] = 0
                kmer_counts[kmer] += 1

    kmers = [kmer for kmer in kmers if kmer_counts[kmer] > 2]


    # this was for keeping track of how many types each kmer occurred
    # counts = []
    # for kmer in kmer_counts:
    #     count = kmer, kmer_counts[kmer]
    #     counts.append(count)
    # counts = sorted(counts, key=lambda x: x[1])
    # counts2 = []
    # for c in counts:
    #     counts2.append(c[1])
    # # list of how many times kmers appeared (# of kmers once, # of kmers twice, etc...)
    # counts3 = [len(list(b)) for a, b in itertools.groupby(counts2)]
    # print counts3


    edges = {}
    for kmer in kmers:
        prefix = kmer[:-1]
        suffix = kmer[1:]
        if prefix not in edges:
            edges[prefix] = []
        # if suffix not in edges[prefix]:
        #     edges[prefix].append(suffix)
        edges[prefix].append(suffix)

    for prefix in sorted(edges.keys()):
        # print prefix + ' -> ' + ','.join(sorted(edges[prefix]))
        pass

    edge_dict = {}
    for kmer in kmers:
        head = kmer[:len(kmer) - 1]
        tail = kmer[1:]
        add_nodes(nodes, head, tail)
        if head not in edge_dict:
            edge_dict[head] = []
        edge_dict[head].append(tail)

    for n in nodes:
        node = nodes[n]
        node['branching'] = not (len(set(node['out_nodes'])) == 1 and len(set(node['in_nodes'])) == 1)

    # go through each branching node and start a new contig
    branching_nodes = [node for node in nodes if nodes[node]['branching']]
    contigs = []
    for node in branching_nodes:
        if node in edge_dict:
            for connected_node in edge_dict[node]:
                contig = [node, connected_node]
                contig = continue_contig(contig)
                contigs.append(contig)

    # print ''
    # print '\n'.join(set(contigs))
    stats[k] = get_stats(contigs)

for k in stats:
    print 'Kmer size: {}'.format(k)
    print '\t{} contigs'.format(stats[k][0])
    print '\tavg contig length: {}'.format(stats[k][1])
    print '\tlongest contig: {}'.format(stats[k][2])
    print ''
