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
        print("Connected!")

        self.cursor.execute("SELECT @@VERSION")
        print(self.cursor.fetchone())
        print(pyodbc.version)

    def create_match(
            self,
            video_name,
            fps,
            width,
            height
    ):
        try:
            self.cursor.execute("""
                INSERT INTO Matches
                (video_name, fps, frame_width, frame_height)
                OUTPUT INSERTED.match_id
                VALUES (?, ?, ?, ?)
            """, (
                str(video_name),
                int(fps),
                int(width),
                int(height)
            ))

            row = self.cursor.fetchone()
            self.conn.commit()

            print("Returned row:", row)

            return row[0]

        except Exception as e:
            print("Exception type:", type(e))
            print("Exception:", repr(e))

            if hasattr(e, "args"):
                print("Args:", e.args)

            raise

    # def create_match(
    #         self,
    #         video_name,
    #         fps,
    #         width,
    #         height
    # ):
    #     self.cursor.execute("""
    #         INSERT INTO Matches
    #         (video_name, fps, frame_width, frame_height)
    #         OUTPUT INSERTED.match_id
    #         VALUES (?, ?, ?, ?)
    #     """, (
    #         video_name,
    #         fps,
    #         width,
    #         height
    #     ))
    #
    #     return self.cursor.fetchone()[0]

    def insert_player(
            self,
            frame_num,
            track_id,
            bbox,
            match_id
    ):
        self.cursor.execute("""
        INSERT INTO Players
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            frame_num,
            track_id,
            bbox[0],
            bbox[1],
            bbox[2],
            bbox[3],
            match_id
        ))

    def insert_ball(
            self,
            frame_num,
            bbox,
            match_id
    ):
        self.cursor.execute("""
        INSERT INTO Ball
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            frame_num,
            bbox[0],
            bbox[1],
            bbox[2],
            bbox[3],
            match_id
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