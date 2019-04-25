# Paper Bin
Misc

## Challenge 

defund accidentally deleted all of his math papers! Help recover them from his computer's raw data.

Author: defund

## Hint

File carving

## Solution

Extract files using foremost

	$ foremost paper_bin.dat 
	Processing: paper_bin.dat
	|*|

The read out all files

	$ for file in *.pdf; do pdftotext $file - | grep actf; done
	actf{proof by triviality}

## Flag

	actf{proof_by_triviality}
