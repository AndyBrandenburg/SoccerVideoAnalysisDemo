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

        self.conn.commit()

    def insert_player(
            self,
            frame_num,
            track_id,
            bbox
    ):
        self.cursor.execute("""
        INSERT INTO players
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            frame_num,
            track_id,
            bbox[0],
            bbox[1],
            bbox[2],
            bbox[3]
        ))

    def insert_ball(
            self,
            frame_num,
            bbox
    ):
        self.cursor.execute("""
        INSERT INTO ball
        VALUES (?, ?, ?, ?, ?)
        """, (
            frame_num,
            bbox[0],
            bbox[1],
            bbox[2],
            bbox[3]
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