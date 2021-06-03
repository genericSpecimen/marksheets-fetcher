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

## Motivation

Approximately in mid-2018, when I was in the second semester of my undergraduate studies, our semester results were out and I was trying to access the marksheet portal, which was succumbing to the load of many students concurrently trying to fetch their marksheets. It was quite a tiring process. One of my friends said, "It would be convenient if we could somehow automate this". From this thought, the idea for this application was born. At that time, I didn't know much about how the internet works, and I had no idea how I would even start to automate a process like this. I only knew how to write simple programs. Nevertheless, I tried to piece together things I found on the internet, and somehow, I managed to make a [working application](https://github.com/genericSpecimen/scrapy-scripts/tree/master/results) but I didn't properly understand how it worked.

Fast forward to today, I now understand the basics of "how the internet works". Therefore, I thought of rewriting this application. The rewritten application was definitely an improvement, which includes the better management of directory structure, general code quality improvements, and, better maintainability. But possibly the biggest improvement is that now I understand how it works. The HTTP Request / Response cycle, GET and POST methods, and things like that, are now clearer.

`
