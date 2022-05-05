  {{ config(materialized='table') }}

  SELECT
     k.keyword,
     c.region,
     COUNT(*) as region_cards_count,
     SUM(CASE WHEN c.keywords LIKE '%' || k.keyword || '%' THEN 1 ELSE 0 END) AS keyword_occurence,
     (SUM(CASE WHEN c.keywords LIKE '%' || k.keyword || '%' THEN 1 ELSE 0 END)::decimal / COUNT(*)::decimal)::decimal(4, 2) AS keyword_perc_of_total_cards
  FROM
      {{ ref('keywords') }} k
          CROSS JOIN {{ ref('cards') }} c
  WHERE
      keyword <> ''
  GROUP BY
      k.keyword,
      c.region
