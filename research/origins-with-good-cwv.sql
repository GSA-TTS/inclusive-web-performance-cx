CREATE TEMP FUNCTION IS_GOOD(good FLOAT64, needs_improvement FLOAT64, poor FLOAT64) RETURNS BOOL AS (
  good / (good + needs_improvement + poor) >= 0.75
);

CREATE TEMP FUNCTION IS_NON_ZERO(good FLOAT64, needs_improvement FLOAT64, poor FLOAT64) RETURNS BOOL AS (
  good + needs_improvement + poor > 0
);

SELECT
  date,
  client,
  COUNT(DISTINCT url) AS origins,
  COUNT(DISTINCT IF(good_inp, url, NULL)) AS origins_with_good_inp,
  COUNT(DISTINCT IF(good_cls, url, NULL)) AS origins_with_good_cls,
  COUNT(DISTINCT IF(good_ttfb, url, NULL)) AS origins_with_good_ttfb,
  COUNT(DISTINCT IF(good_fcp, url, NULL)) AS origins_with_good_fcp,
  COUNT(DISTINCT IF(good_lcp, url, NULL)) AS origins_with_good_lcp,
  COUNT(DISTINCT IF(any_inp, url, NULL)) AS origins_with_any_inp,
  COUNT(DISTINCT IF(any_cls, url, NULL)) AS origins_with_any_cls,
  COUNT(DISTINCT IF(any_ttfb, url, NULL)) AS origins_with_any_ttfb,
  COUNT(DISTINCT IF(any_fcp, url, NULL)) AS origins_with_any_fcp,
  COUNT(DISTINCT IF(any_lcp, url, NULL)) AS origins_with_any_lcp,
  COUNT(DISTINCT IF(good_cwv, url, NULL)) AS origins_with_good_cwv,
  COUNT(DISTINCT IF(any_lcp AND any_cls, url, NULL)) AS origins_eligible_for_cwv,
  SAFE_DIVIDE(COUNT(DISTINCT IF(good_ttfb, url, NULL)), COUNT(DISTINCT IF(any_ttfb, url, NULL))) as pct_good_ttfb,
  SAFE_DIVIDE(COUNT(DISTINCT IF(good_fcp, url, NULL)), COUNT(DISTINCT IF(any_fcp, url, NULL))) as pct_good_fcp,
  SAFE_DIVIDE(COUNT(DISTINCT IF(good_lcp, url, NULL)), COUNT(DISTINCT IF(any_lcp, url, NULL))) as pct_good_lcp,
  SAFE_DIVIDE(COUNT(DISTINCT IF(good_cls, url, NULL)), COUNT(DISTINCT IF(any_cls, url, NULL))) as pct_good_cls,
  SAFE_DIVIDE(COUNT(DISTINCT IF(good_inp, url, NULL)), COUNT(DISTINCT IF(any_inp, url, NULL))) as pct_good_inp,
  SAFE_DIVIDE(COUNTIF(good_cwv), COUNTIF(any_lcp AND any_cls)) AS pct_eligible_origins_with_good_cwv
FROM (
  SELECT
    date,
    CONCAT(origin, '/') AS url,
    IF(device = 'desktop', 'desktop', 'mobile') AS client,
    IS_NON_ZERO(fast_inp, avg_inp, slow_inp) AS any_inp,
    IS_GOOD(fast_inp, avg_inp, slow_inp) AS good_inp,
    IS_NON_ZERO(small_cls, medium_cls, large_cls) AS any_cls,
    IS_GOOD(small_cls, medium_cls, large_cls) AS good_cls,
    IS_NON_ZERO(fast_lcp, avg_lcp, slow_lcp) AS any_lcp,
    IS_GOOD(fast_lcp, avg_lcp, slow_lcp) AS good_lcp,
    IS_NON_ZERO(fast_ttfb, avg_ttfb, slow_ttfb) AS any_ttfb,
    IS_GOOD(fast_ttfb, avg_ttfb, slow_ttfb) AS good_ttfb,
    IS_NON_ZERO(fast_fcp, avg_fcp, slow_fcp) AS any_fcp,
    IS_GOOD(fast_fcp, avg_fcp, slow_fcp) AS good_fcp,
    (IS_GOOD(fast_inp, avg_inp, slow_inp) OR fast_inp IS NULL) AND
    IS_GOOD(small_cls, medium_cls, large_cls) AND
    IS_GOOD(fast_lcp, avg_lcp, slow_lcp) AS good_cwv
  FROM
    `chrome-ux-report.materialized.device_summary`
  WHERE
    date >= '2024-01-01'
)
GROUP BY
  date,
  client
