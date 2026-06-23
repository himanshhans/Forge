# Gallery has no models of its own — it queries Portfolio directly
# (see views.py). The old `showcase_index` SQL view was removed in
# portfolios migration 0003 to avoid SQLite schema-change conflicts.
