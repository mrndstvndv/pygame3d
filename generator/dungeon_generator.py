import random


class DungeonGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 10
        self.min_room_size = 5
        self.max_room_size = 12
        self.max_rooms = 10
        self.rooms = []
        self.spawn = (0, 0)
        self.grid = [[1 for _ in range(width)] for _ in range(height)]

    def generate_room(self):
        width = random.randint(self.min_room_size, self.max_room_size)
        height = random.randint(self.min_room_size, self.max_room_size)
        x = random.randint(0, self.width - width - 1) + 1
        y = random.randint(0, self.height - height - 1) + 1
        return (x, y, width, height)

    def generate_dungeon(self):
        first_room = True

        for i in range(self.max_rooms):
            room = self.generate_room()

            if self.place_room(room):
                if len(self.rooms) > 0:
                    self.connect_rooms(self.rooms[-1], room)
                self.rooms.append(room)

        first_room = self.rooms[0]
        # set spawn
        spawn_x = first_room[0] + first_room[2] // 2
        spawn_y = first_room[1] + first_room[3] // 2

        self.clean_grid()

        self.spawn = (spawn_x, spawn_y)
        self.grid[spawn_y][spawn_x] = 2  # Set spawn point


    def clean_grid(self):
        """Remove redundant corridor tiles that are completely surrounded by other corridor/room tiles."""
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
        # Include diagonals in the neighbor check
        neighbors = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
        
        for j in range(self.height):
            for i in range(self.width):
                if self.grid[j][i] == 1:
                    # Always keep edge tiles
                    if i == 0 or i == self.width-1 or j == 0 or j == self.height-1:
                        new_grid[j][i] = 1
                        continue
                    
                    # Check if this tile is adjacent to at least one empty space (0)
                    has_adjacent_empty = False
                    for dy, dx in neighbors:
                        ny, nx = j + dy, i + dx
                        if (0 <= ny < self.height and 
                            0 <= nx < self.width and 
                            self.grid[ny][nx] == 0):
                            has_adjacent_empty = True
                            break
                    
                    if has_adjacent_empty:
                        new_grid[j][i] = 1
        
        self.grid = new_grid

    def connect_rooms(self, room1, room2):
        x1, y1, width1, height1 = room1
        x2, y2, width2, height2 = room2

        start_x, start_y = x1 + width1 // 2, y1 + height1 // 2
        end_x, end_y = x2 + width2 // 2, y2 + height2 // 2

        # Move horizontally first
        for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
            self.grid[start_y][x] = 0

        # Move vertically
        step = 1 if end_y >= start_y else -1
        for y in range(start_y, end_y + step, step):
            self.grid[y][end_x] = 0

    def place_room(self, room):
        x, y, width, height = room
        # Check if room overlaps with existing corridors
        for j in range(y, y + height):
            for i in range(x, x + width):
                if j >= self.height or i >= self.width or self.grid[j][i] == 0:
                    return False

        # Place the room
        for j in range(y, y + height):
            for i in range(x, x + width):
                self.grid[j][i] = 0  # Wall

        return True


if __name__ == "__main__":
    generator = DungeonGenerator(80, 60)
    generator.generate_dungeon()
    generator.clean_grid()

    for i in generator.grid:
        print("".join(" " if str(cell) == "0" else str(cell) for cell in i))
