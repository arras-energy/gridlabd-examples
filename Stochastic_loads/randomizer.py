# load randomizer
# 
# Note: The IEEE 13 bus model does not appear to have time-sensitive object
# and therefore restoring the initial value is not necessary. If this were
# needed, this implementation would have to address how these time-sensitive
# object respond to the load change.
#

import sys

properties = [
    # properties we intend to manipulate
    "constant_power_A", "constant_power_B", "constant_power_C",
    "constant_current_A", "constant_current_B", "constant_current_C",
    "constant_impedance_A", "constant_impedance_B", "constant_impedance_C",
    ]

accessor = {} # getters for properties we intend to manipulate
initial_value = {} # initial values of loads we will need to use repeatedly

def init(obj:str,t:int) -> int:
    """Initialization of randomizer objects"""

    # get the parent object
    parent = gldcore.get_value(obj,"parent")
    initial_value[obj] = {"parent":parent} # save for use in precommit (performance boost)

    # save the initial value of the target properties
    initial_value[parent] = {x:complex(gldcore.get_value(parent,x).split()[0]) for x in properties}
    
    # fast accessors for randomizer and load object
    accessor[obj] = {"scale":gldcore.property(obj,"scale")}
    accessor[parent] = {x:gldcore.property(parent,x) for x in properties}
    
    return 0 # 0 is ok, 1 is failed

def precommit(obj:str,t:int) -> int:
    """Update of load object based on randomizer state"""

    parent = initial_value[obj]["parent"]
    scale = accessor[obj]["scale"].get_value();

    # scan the properties
    for prop,getter in accessor[parent].items():
        base = initial_value[parent][prop]
        if abs(base) > 0.0: # don't update values unnecessarily
            update = base * ( 1/scale if "impedance" in prop else scale) # impedance response is inverted w.r.t power and current
            accessor[parent][prop].set_value(update)
    
    return gldcore.NEVER # let the randomvar determine the update time
