import pyodbc


class SQLServerManager:

    def __init__(self):

        self.conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=ANDYS_DELL;"
            "DATABASE=SoccerAnalytics;"
            "Trusted_Connection=yes;"
        )

        self.cursor = self.conn.cursor()

    def insert_player(
            self,
            frame_num,
            track_id,
            bbox
    ):
        self.cursor.execute("""
        INSERT INTO Players
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
        INSERT INTO Ball
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
        FROM Players
        WHERE track_id = ?
        ORDER BY frame_num
        """, (1,))

        positions = self.cursor.fetchall()

        for row in positions[:10]:
            print(row)

        print("---COUNT OF ALL PLAYERS---")

        self.cursor.execute("""
        SELECT COUNT(*)
        FROM Players
        """)

        player_count = self.cursor.fetchone()

        print("Player detections:", player_count[0])

        print("---MOST VISIBLE PLAYER---")

        self.cursor.execute("""
        SELECT track_id,
               COUNT(*) AS appearances
        FROM Players
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