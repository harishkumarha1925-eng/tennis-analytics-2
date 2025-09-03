LIST_COMPETITIONS = """
SELECT c.competition_name, cat.category_name
FROM Competitions c
JOIN Categories cat ON c.category_id = cat.category_id;
"""

COUNT_COMPETITIONS_BY_CATEGORY = """
SELECT cat.category_name, COUNT(c.competition_id) AS num_competitions
FROM Competitions c
JOIN Categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name;
"""

TOP_RANKED_COMPETITORS = """
SELECT c.name, c.country, r.rank, r.points
FROM Competitor_Rankings r
JOIN Competitors c ON c.competitor_id = r.competitor_id
ORDER BY r.rank ASC LIMIT 10;
"""

COUNTRY_ANALYSIS = """
SELECT c.country, COUNT(*) as num_competitors, AVG(r.points) as avg_points
FROM Competitors c
JOIN Competitor_Rankings r ON c.competitor_id = r.competitor_id
GROUP BY c.country ORDER BY avg_points DESC;
"""
