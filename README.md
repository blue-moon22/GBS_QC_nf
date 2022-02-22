# GBS QC Nextflow Pipeline for farm5

## About

This pipeline runs QC for lanes of Group B Strep sequences that are imported on farm5 and available on `pf`.

## Installation

1. Download pipeline in a directory where you keep your software or pipelines:
```bash
git clone https://github.com/blue-moon22/GBS_QC_nf.git
```


## Usage
1. Go into pipeline directory
```bash
cd GBS_QC_nf
```

2. Load nextflow module
```bash
module load nextflow/20.10.0-5430
```

3. Run QC analysis using bsub:
```bash
bsub -G team284 -o gbs_qc.o -e gbs_qc.e -R"select[mem>4000] rusage[mem=4000]" -M4000 'nextflow run main.nf --qc_report /path/to/gbs_qc_report.txt --lanes /path/to/gbs_lanes.txt'
```
Change:
- `/path/to/gbs_lanes.txt` to the file location of your list of lanes (that are imported and can be accessed via `pf`), e.g.

```bash
20280_5#1
20280_5#10
20280_5#100
20280_5#101
20280_5#102
20280_5#103
20280_5#104
20280_5#105
20280_5#106
20280_5#107
```

- `/path/to/gbs_qc_report.txt` to the desired location of your output report.

## Output
You should get an tab-delimited output report with the `lane_id`, `rel_abundance` and `rel_abundance_status` (either PASS or FAIL). If there are missing data e.g. `fake_lane#1` then this lane may not have been imported/imported properly with a kraken report, so contact `path-help@sanger.ac.uk` for help with this.
```
lane_id rel_abundance   rel_abundance_status
20280_5#106     93.78   PASS
20280_5#103     90.92   PASS
20280_5#104     98.77   PASS
20280_5#107     93.09   PASS
20280_5#101     90.31   PASS
20280_5#105     93.87   PASS
20280_5#10      95.54   PASS
20280_5#1       95.69   PASS
fake_lane#1
20280_5#102     91.55   PASS
20280_5#100     93.46   PASS
```

## Additional options
    --rel_abund_threshold     Pass read QC if rel_abundance is > rel_abund_threshold. (Default: 70)
    --species                 Species of interest. (Default: 'Streptococcus agalactiae')

### For developers

Run tests:
```
pytest tests
```