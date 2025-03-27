from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

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
        
        frontier = StackFrontier()
        frontier.add(node)
        
        while True:
            if(frontier.is_empty()):
                return NoSolution(explored)
            frontier_node = frontier.remove()
            if frontier_node in explored:
                continue
            explored[frontier_node.state] = True
            neighbours = grid.get_neighbours(frontier_node.state)
            for action, state in neighbours.items():
                if state not in explored:
                    new_node = Node("", state, frontier_node.cost + grid.get_cost(state), frontier_node, action)
                    if grid.end == new_node.state:
                        return Solution(new_node, explored)
                    frontier.add(new_node)