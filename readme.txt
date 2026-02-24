-- sql querys for database:

DELETE FROM airport
WHERE
    id NOT IN(
        2214,
        2218,
        2385,
        2398,
        3431,
        3454,
        2718,
        3070,
        5627,
        3360,
        2655,
        2660,
        2653,
        2652,
        4509,
        4525,
        5226,
        5235,
        2690,
        2691,
        5906,
        5897,
        3077,
        4000,
        5255,
        5279,
        1993,
        1662,
        2688,
        2688,
        4156,
        4060,
        2307,
        2726,
        2341,
        2701,
        2652,
        2542,
        2561,
        3105,
        2767
    );

DELETE FROM game;

DELETE FROM goal_reached;

DELETE FROM goal;

DELETE FROM country
WHERE
    country.iso_country NOT IN(
        SELECT airport.iso_country
        FROM airport
    );

ALTER TABLE goal DROP COLUMN description;

ALTER TABLE goal DROP COLUMN icon;

ALTER TABLE goal DROP COLUMN target;

ALTER TABLE goal DROP COLUMN target_minvalue;

ALTER TABLE goal DROP COLUMN target_maxvalue;

ALTER TABLE goal DROP COLUMN target_text;

ALTER TABLE goal RENAME COLUMN name TO puzzle_piece;

ALTER TABLE airport ADD puzzle_piece int(11);

ALTER TABLE game DROP COLUMN co2_consumed;

ALTER TABLE game RENAME COLUMN co2_budget TO money;

ALTER TABLE game MODIFY id VARCHAR(40) NOT NULL DEFAULT(UUID());

ALTER TABLE airport ADD quiz int(11);

ALTER TABLE goal RENAME TABLE puzzle_pieces;

CREATE TABLE quizzes (
    id int NOT NULL,
    quiz varchar(40),
    CONSTRAINT PK_Person PRIMARY KEY (id)
);

DROP TABLE goal_reached;

ALTER TABLE quizzes ADD answered boolean DEFAULT(0);

ALTER TABLE puzzle_pieces ADD acquired boolean DEFAULT(0);

ALTER TABLE airport
ADD CONSTRAINT FK_quiz FOREIGN KEY (quiz) REFERENCES quizzes (id);

ALTER TABLE airport
ADD CONSTRAINT FK_puzzle_piece FOREIGN KEY (puzzle_piece) REFERENCES puzzle_pieces (id);

ALTER TABLE puzzle_pieces MODIFY id INT NOT NULL AUTO_INCREMENT;

ALTER TABLE quizzes MODIFY id INT NOT NULL AUTO_INCREMENT;

ALTER TABLE player MODIFY id varchar(40) NOT NULL DEFAULT(UUID());

INSERT INTO
    puzzle_pieces (puzzle_piece, aquired)
VALUES (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0);

INSERT INTO
    quizzes (quiz, answered)
VALUES (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0),
    (NULL, 0);