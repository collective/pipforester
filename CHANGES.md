## Changes

## 1.0.2 (unreleased)


- add a `--select`/`-s` option to only fail on cycles the given distribution takes part in,
  so a package is not blocked by cycles it cannot fix. Fixes #6. [@remdub]


## 1.0.1 (2023-07-14)

- use transitive_reduction from the NetworkX module to speed up edge removal. [@gogobd]

### 1.0.0 (2023-05-16)

- fix the cyclic dependency display to show all edges of a cycle in dark violet. [@jensens]
- fix graph of cycles not to show graph multiple times. [@jensens]

### 1.0.0a1 (2023-05-15)

- initial code [@jensens]
