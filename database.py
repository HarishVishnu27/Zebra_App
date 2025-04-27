import sqlite3
from datetime import datetime
from config import DATABASE

def init_db(database_name=DATABASE):
    """Initialize database with required tables."""
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    # Zebra Crossing Table
    for cam_id in range(1, 5):
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS zebra_crossing_data_cam{cam_id} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                vehicle_type TEXT NOT NULL,
                vehicle_count INTEGER NOT NULL
            )
        ''')
    
    conn.commit()
    conn.close()

def save_zebra_crossing_data(cam_id, vehicle_type, vehicle_count):
    """Save Zebra Crossing detection data."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute(f'''INSERT INTO zebra_crossing_data_cam{cam_id}
                           (timestamp, vehicle_type, vehicle_count)
                           VALUES (?, ?, ?)''',
                       (timestamp, vehicle_type, vehicle_count))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error for camera {cam_id}: {e}")
        return False

def get_zebra_crossing_data(cam_id, limit=500):
    """Get Zebra Crossing data for a camera."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        query = f'''
            SELECT 
                timestamp, vehicle_type, 
                COUNT(*) as vehicle_count
            FROM zebra_crossing_data_cam{cam_id}
            GROUP BY timestamp, vehicle_type
            ORDER BY timestamp DESC
            LIMIT {limit}
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        
        processed_rows = [
            {
                'timestamp': row[0],
                'vehicle_type': row[1],
                'vehicle_count': row[2]
            } for row in rows
        ]
        
        conn.close()
        return processed_rows
    except sqlite3.Error as e:
        print(f"Error fetching Zebra Crossing data for camera {cam_id}: {e}")
        return []