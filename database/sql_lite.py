import sqlite3


class SQLiteManager:

    def __init__(self, db_path="sports_db/soccer_tracking.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()


    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            frame_num INTEGER,
            track_id INTEGER,
            x1 REAL,
            y1 REAL,
            x2 REAL,
            y2 REAL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS referees (
            frame_num INTEGER,
            track_id INTEGER,
            x1 REAL,
            y1 REAL,
            x2 REAL,
            y2 REAL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ball (
            frame_num INTEGER,
            x1 REAL,
            y1 REAL,
            x2 REAL,
            y2 REAL
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            match_id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_name TEXT,
            date_run DATETIME DEFAULT CURRENT_TIMESTAMP,
            fps REAL,
            frame_width INTEGER,
            frame_height INTEGER
        );
        """)

        try:
            self.cursor.execute(
                "ALTER TABLE players ADD COLUMN match_id INTEGER"
            )
        except sqlite3.OperationalError:
            pass

        try:
            self.cursor.execute(
                "ALTER TABLE referees ADD COLUMN match_id INTEGER"
            )
        except sqlite3.OperationalError:
            pass

        try:
            self.cursor.execute(
                "ALTER TABLE ball ADD COLUMN match_id INTEGER"
            )

        except sqlite3.OperationalError:
            pass
        #Alters the players table to add pitch_x and pitch_y
        try:
            self.cursor.execute("""
                ALTER TABLE players
                ADD COLUMN pitch_x REAL
            """)
        except sqlite3.OperationalError:
            pass

        try:
            self.cursor.execute("""
                ALTER TABLE players
                ADD COLUMN pitch_y REAL
            """)
        except sqlite3.OperationalError:
            pass
        #Alters the ball table to add pitch_x and pitch_y columns
        try:
            self.cursor.execute("""
                ALTER TABLE ball
                ADD COLUMN pitch_x REAL
            """)
        except sqlite3.OperationalError:
            pass

        try:
            self.cursor.execute("""
                ALTER TABLE ball
                ADD COLUMN pitch_y REAL
            """)
        except sqlite3.OperationalError:
            pass

        ###################-----ADDS NEW TABLES FOR PLAYERS TABLE 7/23/2026-----#########################
        try:
            self.cursor.execute("""
                ALTER TABLE players
                ADD COLUMN team INTEGER
            """)
        except sqlite3.OperationalError:
            pass

        try:
            self.cursor.execute("""
                ALTER TABLE players
                ADD COLUMN team_color_b INTEGER
            """)
        except sqlite3.OperationalError:
            pass

        try:
            self.cursor.execute("""
                ALTER TABLE players
                ADD COLUMN team_color_g INTEGER
            """)
        except sqlite3.OperationalError:
            pass

        try:
            self.cursor.execute("""
                ALTER TABLE players
                ADD COLUMN team_color_r INTEGER
            """)
        except sqlite3.OperationalError:
            pass

        try:
            self.cursor.execute("""
                ALTER TABLE players
                ADD COLUMN has_ball INTEGER
            """)
        except sqlite3.OperationalError:
            pass

        ###CREATE PLAYER STATISTICS TABLE###

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS PlayerStatistics(

            statistic_id INTEGER PRIMARY KEY AUTOINCREMENT,

            match_id INTEGER,

            track_id INTEGER,

            team INTEGER,

            average_pitch_x REAL,

            average_pitch_y REAL,

            touches INTEGER,

            possession_percentage REAL,

            distance_covered REAL,

            recoveries INTEGER,

            interceptions INTEGER,

            top_speed REAL,

            sprint_distance REAL,

            movement_cluster INTEGER,

            FOREIGN KEY(match_id)
                REFERENCES matches(match_id)

        )
        """)

        self.conn.commit()

    def create_match(
            self,
            video_name,
            fps,
            width,
            height
    ):

        self.cursor.execute("""
            INSERT INTO matches
            (
                video_name,
                fps,
                frame_width,
                frame_height
            )
            VALUES (?, ?, ?, ?)
        """, (
            video_name,
            fps,
            width,
            height
        ))


        self.conn.commit()

        return self.cursor.lastrowid

    def insert_player(
            self,
            frame_num,
            track_id,
            bbox,
            match_id,
            pitch_x,
            pitch_y,
            team,
            team_color,
            has_ball
    ):
        self.cursor.execute("""
        INSERT INTO players
        (
            frame_num,
            track_id,
            x1,
            y1,
            x2,
            y2,
            match_id,
            pitch_x,
            pitch_y,
            team,
            team_color_b,
            team_color_g,
            team_color_r,
            has_ball
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            frame_num,
            track_id,
            bbox[0],
            bbox[1],
            bbox[2],
            bbox[3],
            match_id,
            float(pitch_x),
            float(pitch_y),
            int(team) if team is not None else None,

            int(team_color[0]) if team_color is not None else None,
            int(team_color[1]) if team_color is not None else None,
            int(team_color[2]) if team_color is not None else None,

            int(has_ball)

        ))

    def insert_ball(
            self,
            frame_num,
            bbox,
            match_id,
            pitch_x,
            pitch_y
    ):
        self.cursor.execute("""
        INSERT INTO ball
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            frame_num,
            bbox[0],
            bbox[1],
            bbox[2],
            bbox[3],
            match_id,
            float(pitch_x),
            float(pitch_y)
        ))

    def insert_player_statistics(
            self,
            match_id,
            stats
    ):

        self.cursor.execute("""

        INSERT INTO PlayerStatistics(

            match_id,
            track_id,
            team,
            average_pitch_x,
            average_pitch_y,
            touches,
            possession_percentage,
            distance_covered
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        """, (
            match_id,
            stats["track_id"],

            stats["team"],

            stats["average_pitch_x"],

            stats["average_pitch_y"],

            stats["touches"],

            stats["possession"],

            stats["distance"]

        ))

    def player_info(self):

        print("---PLAYER POSITIONS---")

        self.cursor.execute("""
        SELECT frame_num, x1, y1, x2, y2
        FROM players
        WHERE track_id = ?
        ORDER BY frame_num
        """, (1,))

        positions = self.cursor.fetchall()

        for row in positions[:10]:
            print(row)

        print("---COUNT OF ALL PLAYERS---")

        self.cursor.execute("""
        SELECT COUNT(*)
        FROM players
        """)

        player_count = self.cursor.fetchone()

        print("Player detections:", player_count[0])

        print("---MOST VISIBLE PLAYER---")

        self.cursor.execute("""
        SELECT track_id,
               COUNT(*) AS appearances
        FROM players
        GROUP BY track_id
        ORDER BY appearances DESC
        LIMIT 10
        """)

        results = self.cursor.fetchall()

        for row in results:
            print(row)

    def save(self):
        self.conn.commit()

    def close(self):
        self.conn.close()