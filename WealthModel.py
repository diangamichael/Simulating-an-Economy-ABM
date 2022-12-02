import random
import math
import mesa

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

#Global variables
treasury = 0
economy_scale = 100
project_participation = 0

def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return (1 + (1 / N) - 2 * B)


class WealthModel(Model):
    """A model with 10000 number of agents."""
    global treasury
    def __init__(self, N, width, height):
        self.num_agents = N
        self.running = True
        self.grid = MultiGrid(height, width, True)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Wealth": lambda a: a.wealth}
        )
        # Create agents
        for i in range(self.num_agents):
            a = WealthAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def run_model(self, n):
        for i in range(n):
            self.step()
            print("step = ", step())
            """tax_period = step()%10
            if tax_period == 0
                return_tax(self, treasury)"""


class WealthAgent(Agent):
    """ An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1
        x = random.randint(0, self.model.grid.width-1)
        y = random.randint(0, self.model.grid.height-1)
        #print("X Y", x, "and", y)
        if self.model.grid.is_cell_empty([x,y]) == False:
            rich_pos = (x,y)
            rich_receivers = self.model.grid.get_cell_list_contents(rich_pos)
            rich = random.choice(rich_receivers)
            inequality_c = 4
            rich.wealth += inequality_c


    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    ## Daily expenses To trading 
  
    def daily_transactions(self, coins):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = random.choice(cellmates)
            other.wealth += coins
            self.wealth -= coins

  
    

    ## Taxes
   
    def collect_tax(self):
        global treasury
        tax_c = 0
        tax_r = 0.10
        if self.wealth > tax_c:
            tax = math.floor(tax_r*self.wealth)
            treasury += tax
            self.wealth -= tax
            print("I, member", self.pos, "have been taxed , paid", tax, "coin")
            print("TREASURY =", treasury)


    ## Reward agents
    
    def project_reward(self, width, height):
        global treasury
        global project_participation
        treasury_c = 0
        if treasury > treasury_c:
            self.grid = MultiGrid(height, width, True)
            x = random.randint(0, self.grid.width)
            y = random.randint(0, self.grid.height)
            #print("EMPTY = ", self.model.grid.is_cell_empty([x,y]))

            if self.model.grid.is_cell_empty([x,y]) == False:
                position = (x,y)
                potential_receivers = self.model.grid.get_cell_list_contents(position)
                receiver = random.choice(potential_receivers)
                reward_c = 2
                receiver.wealth += reward_c
                treasury -= reward_c
                project_participation += 1
                print("After reward, I own this much =", receiver.wealth)
                print("TOTAL PARTICIPANTS = ", project_participation)

    def step(self):
        #self.move()
        if self.wealth > 0:
            expenditure_c = 5
            self.daily_transactions(expenditure_c)
            self.collect_tax()
            self.project_reward(economy_scale,economy_scale)
            #print("------------step------------")
