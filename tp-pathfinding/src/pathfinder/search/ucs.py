from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

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
        frontier = PriorityQueueFrontier()
        frontier.add(node, node.cost)
        
        while not frontier.is_empty():
            queue_node = frontier.pop()
            if grid.end == queue_node.state:
                return Solution(queue_node, explored)
            for action, state in grid.get_neighbours(queue_node.state).items():
                cost = queue_node.cost + grid.get_cost(state)
                if(state not in explored or cost < explored[state]):
                    new_node = Node("", state, cost, queue_node, action)
                    explored[state] = cost
                    frontier.add(new_node, cost)
        return NoSolution(explored)
