-- models/summarize_plays_by_game.sql

WITH play_by_play AS (
    SELECT
        GameId,
        GameDate,
        OffenseTeam,
        DefenseTeam,
        COUNT(*) AS total_plays,
        AVG(Yards) AS avg_yards,
        SUM(CASE WHEN IsPenaltyAccepted = 1 THEN 1 ELSE 0 END) AS total_penalties
    FROM `sincere-nirvana-340100.nfl_dataset.pbp_2013`
    GROUP BY GameId, GameDate, OffenseTeam, DefenseTeam
)

SELECT
    GameId,
    PARSE_DATE('%m/%d/%y', GameDate) AS GameDate,
    OffenseTeam,
    DefenseTeam,
    total_plays,
    avg_yards,
    total_penalties
FROM play_by_play