import random
class Rectangle:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def __repr__(self):
        return f"Rectangle({self.start_x}, {self.start_y}, {self.end_x}, {self.end_y})"
  
# Dungeon generation functions
def generate_dungeon(width, height, room_min_size=3, room_max_size=7, max_rooms=5):
    # Initialize grid filled with walls (1)
    grid = [[1 for _ in range(width)] for _ in range(height)]
    rooms = []
    for _ in range(max_rooms):
        w = random.randint(room_min_size, room_max_size)
        h = random.randint(room_min_size, room_max_size)
        x = random.randint(1, width - w - 2)
        y = random.randint(1, height - h - 2)
        new_room = Rectangle(x, y, x + w - 1, y + h - 1)
        # Skip if overlapping existing rooms (with one-cell buffer)
        if any(r.start_x <= new_room.end_x + 1 and r.end_x >= new_room.start_x - 1
               and r.start_y <= new_room.end_y + 1 and r.end_y >= new_room.start_y - 1
               for r in rooms):
            continue
        # Carve out room
        rooms.append(new_room)
        for i in range(new_room.start_y, new_room.end_y + 1):
            for j in range(new_room.start_x, new_room.end_x + 1):
                grid[i][j] = 0
        # Connect to previous room with corridors
        if len(rooms) > 1:
            prev = rooms[-2]
            x1, y1 = (prev.start_x + prev.end_x) // 2, (prev.start_y + prev.end_y) // 2
            x2, y2 = (new_room.start_x + new_room.end_x) // 2, (new_room.start_y + new_room.end_y) // 2
            if random.choice([True, False]):
                for xi in range(min(x1, x2), max(x1, x2) + 1): grid[y1][xi] = 0
                for yi in range(min(y1, y2), max(y1, y2) + 1): grid[yi][x2] = 0
            else:
                for yi in range(min(y1, y2), max(y1, y2) + 1): grid[yi][x1] = 0
                for xi in range(min(x1, x2), max(x1, x2) + 1): grid[y2][xi] = 0
    return grid, rooms

if __name__ == '__main__':
    dungeon, rooms = generate_dungeon(20, 15, room_min_size=3, room_max_size=7, max_rooms=6)
    # Print dungeon: '.' for floor, '#' for wall
    for row in dungeon:
        print(''.join('.' if cell == 0 else '#' for cell in row))