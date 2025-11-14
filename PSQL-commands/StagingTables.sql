CREATE TABLE staging_competitions (
    competition_id VARCHAR(30) PRIMARY KEY,
    competition_code VARCHAR(100),
    competition_name VARCHAR(100),
    sub_type VARCHAR(100),
    competition_type VARCHAR(100),
    country_id VARCHAR(10),
    country_name VARCHAR(100),
    domestic_league_code VARCHAR(100),
    confederation VARCHAR(100),
    url VARCHAR(1000),
    is_major_national_league BOOLEAN
);

CREATE TABLE staging_clubs (
    club_id VARCHAR(10),
	club_code VARCHAR(100),
	club_name VARCHAR(100),
	domestic_competition_id VARCHAR(30),
	total_market_value numeric(100),
	squad_size numeric(100),
	average_age float(50),
	foreigners_number numeric(50),
	foreigners_percentage float(50),
	national_team_players numeric(50),
	stadium_name VARCHAR(100),
	stadium_seats numeric(30),
	net_transfer_record VARCHAR(50),
	coach_name VARCHAR(30),
	last_season VARCHAR(30),
	filename VARCHAR(300),
	url VARCHAR(1000),
	PRIMARY KEY (club_id)
);

CREATE TABLE staging_players (
	player_id VARCHAR(30),
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	player_name VARCHAR(100),
	last_season INTEGER,
	current_club_id VARCHAR(10) NOT NULL,
	player_code VARCHAR(100),
	country_of_birth VARCHAR(50),
	city_of_birth VARCHAR(100),
	country_of_citizenship VARCHAR(50),
	date_of_birth DATE,
	sub_position VARCHAR(50),
	player_position VARCHAR(30),
	player_foot VARCHAR(10),
	height_in_cm numeric(30),
	contract_expiration_date DATE,
	agent_name VARCHAR(100),
	image_url VARCHAR(1000),
	url VARCHAR(1000),
	current_club_domestic_competition_id VARCHAR(30) NOT NULL,
	current_club_name VARCHAR(100),
	market_value_in_eur numeric(50),
	highest_market_value_in_eur numeric(50),
	PRIMARY KEY (player_id),
	FOREIGN KEY (current_club_id)
		REFERENCES staging_clubs(club_id),
	FOREIGN KEY (current_club_domestic_competition_id)
		REFERENCES staging_competitions(competition_id)
);

CREATE TABLE staging_games (
	game_id VARCHAR(10),
	competition_id VARCHAR(30) NOT NULL,
	game_season VARCHAR(30),
	game_round VARCHAR(30),
	game_date DATE,
	home_club_id VARCHAR(10) REFERENCES staging_clubs(club_id),
	away_club_id VARCHAR(10) REFERENCES staging_clubs(club_id),
	home_club_goals INTEGER,
	away_club_goals INTEGER,
	home_club_position INT,
	away_club_position INT,
	home_club_manager_name VARCHAR(100),
	away_club_manager_name VARCHAR(100),
	stadium VARCHAR(100),
	game_attendance INT,
	referee VARCHAR(50),
	url VARCHAR(1000),
	home_club_formation VARCHAR(50),
	away_club_formation VARCHAR(50),
	home_club_name VARCHAR(100),
	away_club_name VARCHAR(100),
	game_aggregate VARCHAR(10),
	competition_type VARCHAR(100),
	PRIMARY KEY (game_id),
	FOREIGN KEY (competition_id)
		REFERENCES staging_competitions(competition_id)
);

CREATE TABLE staging_game_lineups (
	game_lineups_id VARCHAR(100),
	game_date DATE,
	game_id VARCHAR(10) REFERENCES staging_games(game_id),
	player_id VARCHAR(30) NOT NULL,
	club_id VARCHAR(30) NOT NULL,
	player_name VARCHAR(100),
	lineup_type VARCHAR(50),
	player_position VARCHAR(100),
	lineup_number INT,
	team_captain BOOLEAN,
	PRIMARY KEY (game_lineups_id),
	FOREIGN KEY (player_id)
		REFERENCES staging_players(player_id),
	FOREIGN KEY (club_id)
		REFERENCES staging_clubs(club_id)
);

CREATE TABLE staging_game_events (
	game_event_id VARCHAR(100),
	game_date DATE,
	game_id VARCHAR(10) NOT NULL,
	event_minute INT,
	event_type VARCHAR(50),
	club_id VARCHAR(30) REFERENCES staging_clubs(club_id),
	player_id VARCHAR(30) NOT NULL,
	description VARCHAR(100),
	player_in_id VARCHAR(30) REFERENCES staging_players(player_id),
	player_assist_id VARCHAR(30) REFERENCES staging_players(player_id),
	PRIMARY KEY (game_event_id),
	FOREIGN KEY (player_id)
		REFERENCES staging_players(player_id),
	FOREIGN KEY (game_id)
		REFERENCES staging_games(game_id)
);

CREATE TABLE staging_club_games (
	game_id VARCHAR(10) NOT NULL,
	club_id VARCHAR(10) NOT NULL,
	own_goals INT,
	own_position INT,
	own_manager_name VARCHAR(100),
	opponent_id VARCHAR(10) REFERENCES staging_clubs(club_id),
	opponent_goals INT,
	opponent_position INT,
	opponent_manager_name VARCHAR(100),
	hosting VARCHAR(10),
	is_win BOOLEAN,
	PRIMARY KEY (game_id, club_id),
	FOREIGN KEY (game_id)
		REFERENCES staging_games(game_id),
	FOREIGN KEY (club_id)
		REFERENCES staging_clubs(club_id)
);

CREATE TABLE staging_appearances (
	appearance_id VARCHAR(50),
	game_id VARCHAR(10) REFERENCES staging_games(game_id),
	player_id VARCHAR(30) NOT NULL,
	player_club_id VARCHAR(10) REFERENCES staging_clubs(club_id),
	player_current_club_id VARCHAR(10) REFERENCES staging_clubs(club_id),
	appearances_date DATE,
	player_name VARCHAR(100),
	competition_id VARCHAR(30) NOT NULL,
	yellow_cards INT,
	red_cards INT,
	goals INT,
	assists INT,
	minutes_played INT,
	PRIMARY KEY (appearance_id),
	FOREIGN KEY (player_id)
		REFERENCES staging_players(player_id),
	FOREIGN KEY (competition_id)
		REFERENCES staging_competitions(competition_id)
);

CREATE TABLE staging_played (
	player_id VARCHAR(30),
	game_id VARCHAR(10),
	PRIMARY KEY (player_id, game_id),
	FOREIGN KEY (player_id)
		REFERENCES staging_players(player_id),
	FOREIGN KEY (game_id)
		REFERENCES staging_games(game_id)
);