from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Greedy Best First Search

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
        explored[node.state] = 0
        frontier = PriorityQueueFrontier()
        frontier.add(node, h(node, grid))
        
        while not frontier.is_empty():
            frontier_node = frontier.pop()
            if(grid.end == frontier_node.state): 
                return Solution(frontier_node, explored)
            for action, state in grid.get_neighbours(frontier_node.state).items():
                cost = frontier_node.cost + grid.get_cost(state)
                if state not in explored or cost < explored[state] :
                    new_node = Node("",state,cost,frontier_node,action)
                    explored[state] = cost
                    frontier.add(new_node, h(new_node, grid))
        return NoSolution(explored)

def h(node : Node, grid : Grid) -> int :
    return abs(node.state[0]-grid.end[0]) + abs(node.state[1]-grid.end[1])