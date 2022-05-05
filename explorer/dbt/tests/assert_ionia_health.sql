SELECT
    *
FROM
    {{ ref('cards') }}
WHERE
    health > 6 AND
    region = 'Ionia'
