# 一个可复用生物信息流程结果目录结构

## 背景

开发生物信息流程无外乎跑一些软件，得到一些分析结果。通常情况下，我们会把一个流程分为数个步骤，每个步骤有一个单独的文件夹。例如，我的分析流程第一步运行质控，我就定义一个文件夹叫`1.qc/`，这个步骤产生的所有结果均保存在`1.qc/`文件夹下。下面是我开发的一个Nanopore 16S鉴定流程的结果目录：

```
.
├── 1.qc
│   ├── nanoplot
│   ├── raw_reads.fastq
│   ├── reads.fasta
│   └── reads.filtered.fastq
├── 2.pick-ref
│   ├── blastn.filtered.txt
│   ├── blastn.txt
│   ├── ref.fasta
│   └── ref.fasta.fai
├── 3.align
│   ├── depth.txt
│   ├── minimap2.filtered.bam
│   ├── minimap2.sam
│   ├── minimap2.sorted.bam
│   └── minimap2.sorted.bam.bai
├── 4.variant-calling
│   ├── medaka_consensus.hdf
│   ├── medaka_variant.vcf.gz
│   └── medaka_variant.vcf.gz.csi
├── 5.consensus
│   ├── pre_consensus.fasta
│   └── consensus.fasta
└── 6.assign
    └── blastn.txt
```

## 问题

> 为了方便，以下以bash脚本演示，其实该流程是使用Python写的。

### 第一种复用

质控步骤，我们运行Filtlong过滤reads，然后使用seqtk转换为fasta格式：

```shell
filtlong --min_length 500 --min_mean_q 10 1.qc/raw_reads.fastq > 1.qc/reads.filtered.fastq
seqtk seq -a 1.qc/reads.filtered.fastq > 1.qc/reads.fasta
```

可以看到这里的`1.qc/reads.filtered.fastq`我们写了两次，这个地方是第一种复用。

有人说这个简单，定义变量不就行了：

```shell
raw_reads=1.qc/raw_reads.fastq
reads_filtered=1.qc/reads.filtered.fastq
reads=1.qc/reads.fasta
filtlong --min_length 500 --min_mean_q 10 ${raw_reads} > ${reads_filtered}
seqtk seq -a ${reads_filtered} > ${reads}
```

这种方法的确能马马虎虎地解决第一种复用的问题。为什么说马马虎虎？因为我们的`1.qc/`仍旧写了3次。

### 第二种复用

假如说我们每一步骤都是一个单独的脚本怎么办？

例如，质控步骤是`qc.sh`，选择参考是`pick-ref.sh`。而我们的选择参考需要用质控步骤的`1.qc/reads.fasta`。

```shell
blastn -query 1.qc/reads.fasta -db /path/to/silva -out 2.pick-ref/blastn.txt
```

因为`pick-ref.sh`与`qc.sh`是两个不同的脚本，无法引用`qc.sh`里面的变量，所以`1.qc/reads.fasta`在这个脚本里面又写了一次，这个地方是第二种复用。

有人说，这个也简单，把变量的定义放到一个单独的脚本里面，然后各个脚本去导入。有了这个思想，你就明白`result_dir`想要做什么了。

`result_dir`就是想要这些目录结构**在整个项目中只写一次，包括文件夹名字也只写一次**。

## 安装

```shell
pip install result_dir
```

## 使用

`result_dir`只有两个类`File`和`Dir`，`File`代表文件，`Dir`代表文件夹。

### File

`File`代表项目中的文件。

想要建立一个文件直接实例化`File`就行，例如：

```python
raw_reads = File('raw_reads.fastq')
```

`File`对象是可调用的，调用直接返回该文件的路径：

```python
path = raw_reads()  # path为raw_reads.fastq
```

### Dir

`Dir`代表文件夹。

分为两种情况，如果要建立一个空文件夹，直接实例化`Dir`就行：

```python
Dir('1.qc')
```

如果该文件夹里面还有子文件、子文件夹则需要继承`Dir`，创建`Dir`的子类才行：

```python
class QCDir(Dir):
    raw_reads_file = File('raw_reads.fastq')
    nanoplot_dir = Dir('nanoplot')
    reads_filtered_file = File('reads.filtered.fastq')
    reads_file = File('reads.fasta')
```

`QCDir`是一个文件夹，该文件夹下有一个子文件夹和三个文件。

```python
qc_dir = QCDir('1.qc')  # 即当前目录下的1.qc文件夹
qc_dir = QCDir('/Users/dev/Projects/ont-16s/1.qc')  # 即/Users/dev/Projects/ont-16s下的1.qc
```

`Dir`对象有是可调用的，调用直接返回该文件夹的路径：

```python
path1 = qc_dir()  # path1为1.qc
path2 = qc_dir.nanoplot_dir()  # path2为1.qc/nanoplot
path3 = qc_dir.reads_file()  # path3为1.qc/reads.fasta
```

`Dir`对象还有一个方法`make`，这个方法可以创建该文件夹及其下面的所有子文件夹。

```python
qc_dir.make()
```

### Nanopore 16S鉴定流程结果目录示例

```python
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
  ont_16s_dir.make()   # 创建所有文件夹（包含子文件夹）
  print(ont_16s_dir.pick_ref.blastn_file())
```

