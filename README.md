# marksheets-fetcher

A command line application to automate the fetching of marksheets from a University website.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Features

* Fetch the marksheets for a range of roll numbers.
* Parse the marksheets for a range of roll numbers and store the data in a .csv file. For now, parsing simply scrapes the semester GPA data.
* Supplying only the range of roll numbers is sufficient, since the year, the college id, and the course id can be extracted from the roll numbers (at least in the roll numbers for the CBCS scheme).
* Creates and manages a neat and clean directory structure according to the deconstructed roll number.

## Run it yourself

```bash
# clone the repo
git clone https://github.com/genericSpecimen/marksheets-fetcher.git 

cd marksheets-fetcher/

# create a vitual environment and install dependencies
make start

source env/bin/activate
```

Now we can run our application.

```bash
# fetch marksheets in the range of the specified roll numbers (inclusive)
python marksheets.py --fetch --from 19234747001 --to 19234747055

# parse marksheets in the range of the specified roll numbers (inclusive)
python marksheets.py --parse --from 19234747001 --to 19234747055

```

This will create the following directory structure. The downloaded HTML files will be stored at `DownloadedResults/19/234/747`, and, the parsed data will be stored in a .csv file at the same location.

```
DownloadedResults/
└── 19
    └── 234
        └── 747
```

This way, using information from just the roll numbers, a clean directory structure as shown below can be maintained. This also eases the application's work in traversing files.

```
DownloadedResults/
├── 17
│   ├── 025
│   │   └── 570
│   ├── 035
│   │   └── 570
│   └── 058
│       └── 570
├── 18
│   └── 058
│       └── 570
├── 19
│   └── 234
│       └── 747
```

## Made with

* [requests](https://docs.python-requests.org/en/master/)
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)

