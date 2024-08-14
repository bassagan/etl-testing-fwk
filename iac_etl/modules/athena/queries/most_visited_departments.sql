SELECT
    department,
    COUNT(*) AS total_visits
FROM
    "etl_clean_athena_dev"."curated_visits"
GROUP BY
    department
ORDER BY
    total_visits DESC;
