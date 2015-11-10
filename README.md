# Software Debugging Final Project

We implement HDD: Hierarchical Delta Debugging in ``xmlproc/hdd.py``

Reference: http://web.cs.ucdavis.edu/~su/publications/icse06-hdd.pdf

## Evaluation

after 1000 tests

|                              |ddmin (ms)  |HDD (ms)  |
|------------------------------|-------|-----|
|Balanced                      |20.6   |21.5 |
|Unbalances(fail in depth)     |43.4   |47.8 |
|Unbalances1(fail not in depth)|46.8   |23.4 |
|Unbalances2(fail not in depth)|43.5   |23.0 |

In the worst case, HDD has the same performance as ddmin.

In general case, HDD has great improvement of efficiency.

## Report

See ``report.pdf``.
