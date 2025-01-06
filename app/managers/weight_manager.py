# app/managers/weight_manager.py

import threading

class WeightManager:
    """
    Manages scoring weights with concurrency control.
    """
    def __init__(self):
        self.lock = threading.Lock()
        self.alpha1 = 2.0
        self.alpha2 = 1.0
        self.alpha3 = 1.5
        self.alpha4 = 0.5
        self.alpha5 = 1.0
        self.alpha6 = 1.2
    
    def get_weights(self):
        with self.lock:
            return (self.alpha1, self.alpha2, self.alpha3,
                    self.alpha4, self.alpha5, self.alpha6)
    
    def set_weights(self, alpha1, alpha2, alpha3, alpha4, alpha5, alpha6):
        with self.lock:
            self.alpha1 = alpha1
            self.alpha2 = alpha2
            self.alpha3 = alpha3
            self.alpha4 = alpha4
            self.alpha5 = alpha5
            self.alpha6 = alpha6