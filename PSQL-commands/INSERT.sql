INSERT INTO countries (country_id, country_name)
SELECT DISTINCT country_id, country_name
FROM staging_competitions
WHERE country_id IS NOT NULL;

INSERT INTO competitions (competition_id, competition_name, competition_type, country_id)
SELECT competition_id, competition_name, competition_type, country_id
FROM staging_competitions;

INSERT INTO stadiums (stadium_name, stadium_seats)
SELECT stadium_name, stadium_seats
FROM (
    SELECT stadium_name, stadium_seats,
           ROW_NUMBER() OVER (PARTITION BY stadium_name ORDER BY stadium_seats DESC) AS rn
    FROM staging_clubs
    WHERE stadium_name IS NOT NULL
) AS ranked_stadiums
WHERE rn = 1;

INSERT INTO stadiums (stadium_name, stadium_seats)
SELECT DISTINCT sg.stadium, NULL::INTEGER
FROM staging_games sg
WHERE sg.stadium IS NOT NULL
  AND sg.stadium NOT IN (
      SELECT s.stadium_name FROM stadiums s
  );

INSERT INTO clubs (club_id, club_name, competition_id, squad_size, stadium_name)
SELECT club_id, club_name, domestic_competition_id, squad_size, stadium_name
FROM staging_clubs;

INSERT INTO players (player_id, player_name, last_season, current_club_id, date_of_birth, sub_position, player_position, current_club_domestic_competition_id)
SELECT player_id, player_name, last_season, current_club_id, date_of_birth, sub_position, player_position, current_club_domestic_competition_id
FROM staging_players;

INSERT INTO games (game_id, competition_id, game_date, home_club_id, away_club_id, home_club_goals, away_club_goals, stadium_name, game_attendance)
SELECT game_id, competition_id, game_date, home_club_id, away_club_id, home_club_goals, away_club_goals, stadium, game_attendance
FROM staging_games;

INSERT INTO game_lineups (game_lineups_id, game_id, player_id, club_id)
SELECT game_lineups_id, game_id, player_id, club_id
FROM staging_game_lineups;
