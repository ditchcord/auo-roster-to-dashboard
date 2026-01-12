# auo-roster-to-dashboard

### Compile names in roster to a list of names and pieces they are playing in 

## Obtaining roster data
1. Open symphony roster and control/command+A to highlight everything, then copy it
2. Paste it into an empty .txt file and save it as **symphony.txt**
3. Open chamber orchestra roster and control/command+A to highlight everything, then copy it
4. Paste it into an empty .txt file and save it as **chamber.txt**
5. Write the names of every board member in list format in an empty .txt file and save it as **board.txt**

## Quick start
1. Install Python 3.10 or newer
2. Clone this repository to your device
3. Create a folder called **private** in the repo and move/copy your **symphony.txt** and **chamber.txt** and **board.txt** to that folder (so that git pushes won't expose ppl's data)
4. Open main.py
5. Type the file name of your symphony and chamber rosters and board when prompted
6. Output files will be in a folder titled the current time
7. **names.txt** can be pasted into the first column of the dashboard spreadsheet
8. **pieces.csv** can be pasted in the 

## Troubleshooting
After parsing Cashnet Record - if extra words are appended to people's names, 
or dues appearing in non dues payments, add those words to Tokens.tokens in main.py.

Email wellsjason543 at gmail dot com for issues or questions

## External content
- cmu_csps_utils (for 2d list print) by CMU CS Prep School

#

--Copyright notice does not apply to 'cmu_cpcs_utils.py'--

Copyright (c) 2026 J Wells

MOST RIGHTS RESERVED - DISTRIBUTION PROHIBITED

Permission is hereby granted, free of charge, to any person 
obtaining a copy of this software and associated documentation 
files (the "Software"), to use, modify, or merge the Software on 
their personal computer. The following rights are reserved: To 
publish, distribute, sublicense, and/or sell copies of the 
Software or modified versions of the Software, including 
anything merged with the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
OTHER DEALINGS IN THE SOFTWARE.