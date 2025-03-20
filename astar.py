import heapq


class Node:
    def __init__(self, x, y, cost=0, parent=None):
        self.x = x
        self.y = y
        self.cost = cost  # g-score (distance from start)
        self.parent = parent
        self.heuristic = 0  # h-score (estimated distance to goal)
        self.total_cost = 0  # f-score (g + h)

    def __lt__(self, other):
        return self.total_cost < other.total_cost


def heuristic(a, b):
    """Manhattan distance heuristic for grid traversal."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(grid, start, goal):
    """Finds the shortest path in a grid using A* algorithm."""
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, Node(*start, cost=0))
    closed_set = set()

    while open_set:
        current = heapq.heappop(open_set)

        if (current.x, current.y) in closed_set:
            continue
        closed_set.add((current.x, current.y))

        if (current.x, current.y) == goal:
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1]  # Reverse the path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            nx, ny = current.x + dx, current.y + dy

            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 0:  # Ensure within bounds & not an obstacle
                move_cost = 1 if grid[nx][ny] == -1 else grid[nx][ny]  # Use grid value as cost if positive
                neighbor = Node(nx, ny, cost=current.cost + move_cost, parent=current)
                neighbor.heuristic = heuristic((nx, ny), goal)
                neighbor.total_cost = neighbor.cost + neighbor.heuristic
                heapq.heappush(open_set, neighbor)

    return None  # No path found


def find_nearest_goal(grid, start, goals):
    """Finds the nearest goal using A* distance."""
    best_path = None
    best_goal = None
    best_cost = float('inf')

    for goal in goals:
        path = a_star(grid, start, goal)
        if path and len(path) < best_cost:
            best_cost = len(path)
            best_goal = goal
            best_path = path

    return best_goal, best_path


# Example grid (0 = obstacle, -1 = traversable, positive floats = weighted cost)
grid = [[-1 if (i + j) % 3 else 0 if (i * j) % 5 == 0 else round((i + j) % 10 + 1.1, 1) for j in range(64)] for i in
        range(42)]

start = (0, 0)
goals = [(41, 63), (30, 50), (10, 20)]  # Example set of goals
best_goal, path = find_nearest_goal(grid, start, goals)
print("Nearest Goal:", best_goal)
print("Optimal Path:", path)
