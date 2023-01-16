
from model import Model

class ModelWithMotivation(Model):
    da = 0.5  # distraction activation
    discount = 0.1 # discount due to motivation drop
    
    def discount_goal_activation(self):
        self.ga -= self.discount
        
    def __str__(self):
        return "\n=== Model ===\n" \
        "Time: " + str(self.time) + " s \n" \
        "Goal:" + str(self.goal) + "\n" \
        "DM:" + "\n".join([str(c) for c in self.dm]) + "\n" \
        "ga: " + str(self.ga) + "\n" 
    
    def distraction(self):
        return self.da + self.noise(self.s) > self.ga + self.noise(self.s)