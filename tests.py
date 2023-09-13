# -*- coding: utf-8 -*-
from result_dir import File, Dir


class QCDir(Dir):
    raw_reads_file = File('raw_reads.fastq')
    nanoplot_dir = Dir('nanoplot')
    reads_filtered_file = File('reads.filtered.fastq')
    reads_file = File('reads.fasta')


class PickRefDir(Dir):
    blastn_file = File('blastn.txt')
    filtered_blastn_file = File('blastn.filtered.txt')
    ref_file = File('ref.fasta')


class AlignDir(Dir):
    minimap2_file = File('minimap2.sam')
    filtered_minimap2_file = File('minimap2.filtered.bam')
    sorted_minimap2_file = File('minimap2.sorted.bam')
    depth_file = File('depth.txt')


class VariantCallingDir(Dir):
    medaka_consensus_file = File('medaka_consensus.hdf')
    medaka_variant_file = File('medaka_variant.vcf')
    compressed_medaka_variant_file = File('medaka_variant.vcf.gz')


class ConsensusDir(Dir):
    masked_file = File('masked.fasta')
    pre_consensus_file = File('pre_consensus.fasta')
    consensus_file = File('consensus.fasta')


class AssignDir(Dir):
    blastn_file = File('blastn.txt')


class ONT16SDir(Dir):
    qc = QCDir('1.qc')
    pick_ref = PickRefDir('2.pick-ref')
    align = AlignDir('3.align')
    variant_calling = VariantCallingDir('4.variant-calling')
    consensus = ConsensusDir('5.consensus')
    assign = AssignDir('6.assign')


if __name__ == '__main__':
    ont_16s_dir = ONT16SDir('/Users/dev/Projects/ont_16s')  # 实例化最上层文件夹
    ont_16s_dir.make()  # 创建所有文件夹（包含子文件夹）
    print(ont_16s_dir.pick_ref.blastn_file())
