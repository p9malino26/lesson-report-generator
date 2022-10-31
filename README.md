# Lesson Report Generator
An automated framework for generating reports and receipts for my tutoring sessions.

The Python script prepares two Org mode files, one for the report and one for the payment receipt, by taking the master Org mode files and substituting the text in each section with what is defined in the content file. The generated org mode files can then be converted into LaTeX, and then into PDF.

# Usage

`$ python gen_reports.py --hourly-rates <hourly rates file> <content file>`

Where:
* The hourly rates file contains the hourly rate I charge for each student. A sample hourly rates file is located in this repo.
* The content file contains the information that will be put into both the report and receipt. A sample content file is located in this repo.
