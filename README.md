# Inclusive Web Performance and CX

This project contains research around web performance in the federal government to help hone in on a potential solution that can work at a large scale.

Currently, this project has a `research` directory that uses publicly available data sources to see where the gaps are in the current monitoring strategy for federal sites and applications, particularly for those users who might be on low or mid-tier mobile devices and/or limited data plans.

Here are some of the questions we hope to answer:

Questions to be answered:

- Is the site scan data close to the data in CrUX?
    - Use CrUX API for individual pages
- Are we scanning the right things?
  - How do people experience the urls that are accessed the most?
- How can we help developers do the right thing?
- Top tasks?
  - Can we correlate bounce rate with perf data?
- What other metrics can we collect?
- Are there regions where we're slow?
- Are there things we can do with the cloud.gov platform?
  - 103 early hints
  - Compression
  - Etc
- What APIs aren't we using
  - Modern image formats (avif, webp)
  - Responsive images
  - bfcache
  - 103 Early hints
  - Speculation rules api
  - Observers (intersection, performance, etc)
  - fetchpriority
  - scheduler.yield

## Answered questions

- Look at top 10k. How many of those urls show up in site scan?
- Is CX speed good for the large majority of people? (p99 would be fantastic)
- Where are the gaps in the current strategy?

## Code formatting
To format code, use 

```bash
nbqa black <dir>
```

to lint
```bash
nbqa pylint <dir>
```

Source your venv
```bash
. path/to/venv/bin/activate
```

Install the cli apps
```bash
pip install --editable .
```
