class Node:
    def __init__(self, x_coord, y_coord):
        # Position
        self.x = x_coord
        self.y = y_coord
        # Node type
        self.bObstacle = False
        self.neighbours = []
        # A* computation state
        self.bVisited = False
        self.fGlobalGoal = 0
        self.fLocalGoal = 0
        self.parent = None
    
    
    def __eq__(self, o):
        if o is None:
            return False
        if self is o:
            return True
        return self.fGlobalGoal == o.fGlobalGoal

    
    def __lt__(self, o: object) -> bool:
        return self.fGlobalGoal < o.fGlobalGoal


    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def reset_state_for_astar(self):
        self.bVisited = False
        self.fGlobalGoal = float('inf')
        self.fLocalGoal = float('inf')
        self.parent = None