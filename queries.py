# queries.py

# 1. List all competitions with their category name
LIST_COMPETITIONS = """
SELECT c.competition_name, cat.category_name
FROM Competitions c
JOIN Categories cat ON c.category_id = cat.category_id;
"""

# 2. Count the number of competitions in each category
COUNT_COMPETITIONS_BY_CATEGORY = """
SELECT cat.category_name, COUNT(c.competition_id) AS num_competitions
FROM Competitions c
JOIN Categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name;
"""

# 3. Find all competitions of type 'doubles'
COMPETITIONS_DOUBLES = """
SELECT competition_name, type, gender
FROM Competitions
WHERE type = 'doubles';
"""

# 4. Get competitions that belong to a specific category (e.g., ITF Men)
COMPETITIONS_BY_CATEGORY = """
SELECT competition_name, type, gender
FROM Competitions c
JOIN Categories cat ON c.category_id = cat.category_id
WHERE cat.category_name = %s;
"""

# 5. Identify parent competitions and their sub-competitions
PARENT_SUB_COMPETITIONS = """
SELECT parent.competition_name AS parent_name, child.competition_name AS sub_competition
FROM Competitions child
JOIN Competitions parent ON child.parent_id = parent.competition_id;
"""

# 6. Analyze the distribution of competition types by category
DISTRIBUTION_BY_CATEGORY = """
SELECT cat.category_name, c.type, COUNT(*) as num_competitions
FROM Competitions c
JOIN Categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name, c.type;
"""

# 7. List all competitions with no parent (top-level competitions)
TOP_LEVEL_COMPETITIONS = """
SELECT competition_name
FROM Competitions
WHERE parent_id IS NULL;
"""

# ---------------- Competitor Queries ----------------

# Get all competitors with their ranking and points
ALL_COMPETITORS = """
SELECT c.name, c.country, r.ranking, r.points
FROM Competitor_Rankings r
JOIN Competitors c ON c.competitor_id = r.competitor_id
ORDER BY r.ranking ASC;
"""

# Find top 5 competitors
TOP_5_COMPETITORS = """
SELECT c.name, c.country, r.ranking, r.points
FROM Competitor_Rankings r
JOIN Competitors c ON c.competitor_id = r.competitor_id
ORDER BY r.ranking ASC
LIMIT 5;
"""

# List competitors with no rank movement (stable rank)
STABLE_COMPETITORS = """
SELECT c.name, r.ranking, r.points
FROM Competitor_Rankings r
JOIN Competitors c ON c.competitor_id = r.competitor_id
WHERE r.movement = 0;
"""

# Get total points of competitors from a specific country (e.g., Croatia)
POINTS_BY_COUNTRY = """
SELECT c.country, SUM(r.points) as total_points
FROM Competitors c
JOIN Competitor_Rankings r ON c.competitor_id = r.competitor_id
WHERE c.country = %s
GROUP BY c.country;
"""

# Count the number of competitors per country
COMPETITORS_PER_COUNTRY = """
SELECT c.country, COUNT(*) as num_competitors
FROM Competitors c
GROUP BY c.country;
"""

# Find competitor with the highest points
HIGHEST_POINTS = """
SELECT c.name, c.country, r.points
FROM Competitor_Rankings r
JOIN Competitors c ON c.competitor_id = r.competitor_id
ORDER BY r.points DESC
LIMIT 1;
"""

# Country-wise analysis (total competitors + avg points)
COUNTRY_ANALYSIS = """
SELECT c.country, COUNT(*) as num_competitors, AVG(r.points) as avg_points
FROM Competitors c
JOIN Competitor_Rankings r ON c.competitor_id = r.competitor_id
GROUP BY c.country
ORDER BY avg_points DESC;
"""

