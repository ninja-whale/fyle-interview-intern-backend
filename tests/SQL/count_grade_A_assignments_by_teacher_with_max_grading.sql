WITH TeacherGradingCounts AS (
    SELECT
        teacher_id,
        COUNT(*) AS total_graded
    FROM
        assignments
    WHERE
        state = 'GRADED'
    GROUP BY
        teacher_id
),
TopTeacher AS (
    SELECT
        teacher_id
    FROM
        TeacherGradingCounts
    ORDER BY
        total_graded DESC
    LIMIT 1
)
SELECT
    COUNT(*) AS grade_a_count
FROM
    assignments
WHERE
    teacher_id = (SELECT teacher_id FROM TopTeacher)
    AND grade = 'A';
