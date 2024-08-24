SELECT
    date_trunc('day', appointment_date) AS visit_day,
    COUNT(diagnosis) AS total_diagnoses
FROM
    "etl_clean_athena_dev"."curated_visits"
GROUP BY
    visit_day
ORDER BY
    visit_day;
