SELECT
    doctor_name,
    COUNT(*) AS total_visits
FROM
    "etl_clean_athena_dev"."curated_visits"
GROUP BY
    doctor_name
ORDER BY
    total_visits DESC
LIMIT 10;