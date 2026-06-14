CREATE TABLE countries (
    country_id VARCHAR(255) PRIMARY KEY,
    country_name VARCHAR(255)
);

CREATE TABLE competitions (
    competition_id VARCHAR(255) PRIMARY KEY,
    competition_name VARCHAR(255),
    competition_type VARCHAR(255) NOT NULL,
    country_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(country_id)
);

CREATE TABLE stadiums (
    stadium_name VARCHAR(255) PRIMARY KEY,
    stadium_seats INTEGER
);

CREATE TABLE clubs (
    club_id VARCHAR(255) PRIMARY KEY,
	club_name VARCHAR(255),
	competition_id VARCHAR(255) NOT NULL,
	squad_size INTEGER,
	stadium_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (competition_id) REFERENCES competitions(competition_id),
    FOREIGN KEY (stadium_name) REFERENCES stadiums(stadium_name)
);

CREATE TABLE positions (
    sub_position VARCHAR(255) PRIMARY KEY,
    position VARCHAR(255) NOT NULL
);

CREATE TABLE players (
	player_id VARCHAR(255) PRIMARY KEY,
	player_name VARCHAR(255),
    last_season INTEGER,
	current_club_id VARCHAR(255) NOT NULL,
	date_of_birth DATE,
	sub_position VARCHAR(255),
	current_club_domestic_competition_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (current_club_id) REFERENCES clubs(club_id),
    FOREIGN KEY (current_club_domestic_competition_id) REFERENCES competitions(competition_id),
    FOREIGN KEY (sub_position) REFERENCES positions(sub_position)
);

CREATE TABLE games (
	game_id VARCHAR(255) PRIMARY KEY,
	competition_id VARCHAR(255) NOT NULL,
	game_date DATE,
	home_club_id VARCHAR(255) NOT NULL,
	away_club_id VARCHAR(255) NOT NULL,
	home_club_goals INTEGER,
	away_club_goals INTEGER,
	stadium_name VARCHAR(255) NOT NULL,
	game_attendance INT,
    FOREIGN KEY (competition_id) REFERENCES competitions(competition_id),
    FOREIGN KEY (home_club_id) REFERENCES clubs(club_id),
    FOREIGN KEY (away_club_id) REFERENCES clubs(club_id),
    FOREIGN KEY (stadium_name) REFERENCES stadiums(stadium_name)
);

CREATE TABLE game_lineups (
    game_lineups_id VARCHAR(255) PRIMARY KEY,
    game_id VARCHAR(255) NOT NULL,
    player_id VARCHAR(255) NOT NULL,
    club_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (club_id) REFERENCES clubs(club_id)
);
