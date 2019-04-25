# Blank Paper
Misc

## Challenge 

Someone scrubbed defund's paper too hard, and a few of the bytes fell off.

Author: defund

blank_paper.pdf

## Solution

We can use pdftotext to parse it

	 $ pdftotext blank_paper.pdf 
	Syntax Warning: May not be a PDF file (continuing anyway)

	 $ cat blank_paper.txt | grep actf
	actf{knot very interesting}


## Flag

	actf{knot_very_interesting}
