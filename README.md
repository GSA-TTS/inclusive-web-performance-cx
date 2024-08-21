# Inclusive Web Performance and CX

This project contains research around web performance in the federal government to help hone in on a potential solution that can work at a large scale.

Currently, this project has a `research` directory that uses publicly available data sources to see where the gaps are in the current monitoring strategy for federal sites and applications, particularly for those users who might be on low or mid-tier mobile devices and/or limited data plans.

Here are some of the questions we hope to answer:

Questions to be answered:

- Where are the gaps in the current strategy?
  - Is the site scan data close to the data in CrUX?
    - Use CrUX API for individual pages
- Are we scanning the right things?
  - Look at top 10k. How many of those urls show up in site scan?
  - How do people experience the urls that are accessed the most?
- How can we help developers do the right thing?
- Top tasks?
  - Is it good for the most number of people? (p99) would be great
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
