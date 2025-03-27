from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)
        
        # Initialize the explored dictionary to be empty
        explored = {} 
        
        # Add the node to the explored dictionary
        explored[node.state] = True
        
        if(grid.end == node.state):
            return Solution(node, explored)
        
        frontier = QueueFrontier()
        frontier.add(node)
        
        while True:
            if(frontier.is_empty()):
                return NoSolution(explored)
            frontier_node = frontier.remove()
            actions = grid.get_neighbours(frontier_node.state)
            for action, state in actions.items():
                if state not in explored:
                    new_node  = Node("", state, frontier_node.cost + grid.get_cost(state), frontier_node, action)
                    if(grid.end == new_node.state):
                        return Solution(new_node, explored)
                    explored[new_node.state] = True
                    frontier.add(new_node)
