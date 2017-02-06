

INITIAL_WEIGHT = 0
ACTION_POTENTIAL = 1
RESTING_POTENTIAL = 0
POLARIZATION_SECONDS = 0.5
REFRACTORY_PERIOD = 0.1

import worker_upython


class Worker(worker_upython.Worker):
    
    def __init__(self, server_address, server_port):
        super().__init__(server_address, server_port)
        self.initializeConfig()


    def initializeConfig(self):
        self.config = {'inputs': {},
                       'output': {'value': RESTING_POTENTIAL,
                                  'polarized_time': self.now(),
                                  'lasting': REFRACTORY_PERIOD * 1000}}
        self.emptyLog()

        
    def log(self, message):
        self.logs.append((self.now(), self.name, message))
        
       
    def getConfig(self, ):
        return self.config
      
       
    def getLog(self, ):
        return self.logs
        
        
    def emptyLog(self, ):
        self.logs = []
            
      
    def setConnections(self, connections):
        self.config['connections'] = connections

       
    def getConnections(self, ):
        return self.config.get('connections', {})
        

    def addConnection(self, neuron_id):
        connections = self.getConnections()
        connections[neuron_id] = neuron_id
        self.setConnections(connections)

       
    def deleteConnection(self, neuron_id):
        connections = self.getConnections()
        connections.pop(neuron_id) 
        self.setConnections(connections)

       
    def setWeights(self, weights):
        self.config['weights'] = weights

       
    def getWeights(self, ):
        return self.config.get('weights', {})

       
    def setWeight(self, neuron_id, weight):
        weights = self.getWeights()
        weights[neuron_id] = weight
        self.setWeights(weights)

       
    def getWeight(self, neuron_id):
        return self.getWeights().get(neuron_id, INITIAL_WEIGHT)

       
    def setThreshold(self, threshold):
        self.config['threshold'] = threshold

       
    def getThreshold(self, ):
        return self.config.get('threshold', float("inf"))
        

    def in_refractory_period(self, ):
        output = self.config['output'] 
        
        # 如果 output 還沒有超過有效期
        return True if output['polarized_time'] + output['lasting'] >= self.now() else False
        
        
    def sumInputsAndWeights(self, ):
        weights = self.config.get('weights', {})
        signal_inputs = self.config.get('inputs', {})
        sum_of_weighted_inputs = 0
        currentTime = self.now()
        
        # sum weighted inputs
        for neuron in signal_inputs:
            signal_input = signal_inputs[neuron]
            # if input signal doesn't expire yet
            signal_input['value'] = signal_input.get('value', ACTION_POTENTIAL) if signal_input['kick_time'] + signal_input['lasting'] >= currentTime else RESTING_POTENTIAL
            sum_of_weighted_inputs += signal_input['value'] * weights.get(neuron, INITIAL_WEIGHT)
                    
        return sum_of_weighted_inputs


    def setOutput(self, potential):
        # set output as potential
        self.config['output']['value'] = potential
        self.config['output']['polarized_time'] = self.now()


    def setOutputActive(self, ):
        self.log('Setting output of {0} to ACTION_POTENTIAL.'.format(self.name))
        self.setOutput(ACTION_POTENTIAL)
        

    def getOutput(self, ):
        if self.in_refractory_period():
            output = self.config['output'].get('value', RESTING_POTENTIAL)
        else:
            output = RESTING_POTENTIAL        
        return output    
        

    def receiveInput(self, neuron_id): 
        # recording input
        signal_inputs = self.config.get('inputs', {})
        signal_input = signal_inputs.get(neuron_id)
        
        # the time input was received
        currentTime = self.now()
        
        # no record yet, need to initialize
        if signal_input is None:
            signal_input = {'value': RESTING_POTENTIAL,
                     'kick_time': currentTime,
                     'lasting': POLARIZATION_SECONDS * 1000}
            signal_inputs[neuron_id] = signal_input
        
        remainingValue = signal_input['value'] if signal_input['kick_time'] + signal_input['lasting'] >= currentTime else RESTING_POTENTIAL  # 上一次 input 的殘餘值
        signal_input['value'] = remainingValue + ACTION_POTENTIAL  # cumulate
        signal_input['kick_time'] = currentTime
        signal_input['lasting'] = POLARIZATION_SECONDS * 1000
        

    def kick(self, neuron_id):
        self.log('{0} is kicking {1}.'.format(neuron_id, self.name))     
        
        # recording input
        self.receiveInput(neuron_id)    
        
        sum_of_weighted_inputs = self.sumInputsAndWeights()
        threshold = self.getThreshold()    
        currentOutput = self.getOutput()
        
        if not self.in_refractory_period():
            # refractory period is expired, need to re-evaluate       
            if sum_of_weighted_inputs >= threshold:
                self.fire() 
        else: 
            # currently in refractory period
            self.log('{0} is still in refractory-period.'.format(self.name))
            if currentOutput == ACTION_POTENTIAL:
                # currently at ACTION_POTENTIAL
                if sum_of_weighted_inputs >= threshold:
                    self.log('{0} is still in refractory_period at action potential, then a neuron {1} kicks in, now sum_of_weighted_inputs >= threshold.'.format(self.name, neuron_id))
                else:                
                    self.log('{0} is still in refractory_period at action potential, then a neuron {1} kicks in, now sum_of_weighted_inputs < threshold.'.format(self.name, neuron_id))
            else: 
                # currently at RESTING_POTENTIAL
                if sum_of_weighted_inputs >= threshold:
                    self.log('{0} is still in refractory_period at resting potential, then a neuron {1} kicks in, now sum_of_weighted_inputs >= threshold.'.format(self.name, neuron_id))
                else:                
                    self.log('{0} is still in refractory_period at resting potential, then a neuron {1} kicks in, now sum_of_weighted_inputs < threshold.'.format(self.name, neuron_id))    
                    
       
    def fire(self, ):    
        self.blink_led(times = 1, on_seconds = 0.1, off_seconds = 0.1)
        
        self.log('{0} fires.'.format(self.name))
        self.setOutputActive()  
        
        # kick down-stream neurons
        connections = self.getConnections() 
        for connection in connections.keys():            
            # send message to kick other neurons
            message = {'receiver': connection,
                       'message_type': 'function',
                       'function': 'kick',
                       'kwargs': {'neuron_id': self.name}}
            self.request(message)
