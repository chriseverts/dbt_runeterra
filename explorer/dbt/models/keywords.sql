{{ config(materialized='table') }}

SELECT DISTINCT
    regexp_replace(unnest(string_to_array("keywords", ',')), '[^\w]+','', 'gi') AS keyword
FROM
    {{ ref('cards') }}
