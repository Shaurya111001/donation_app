import smartpy as sp
class EventPlanner(sp.Contract):
    def __init__(self, initialOwner):
        self.init(owner = initialOwner,
                    counter = 0,
                  nameToEvent = sp.map(tkey = sp.TInt))

    @sp.entry_point
    def setAll(self, params):
        sp.verify(sp.sender == self.data.owner)
        self.data.counter = self.data.counter + 1
        self.checkEvent(self.data.counter)
        self.data.nameToEvent[self.data.counter].cause = params.cause
        self.data.nameToEvent[self.data.counter].comp = params.comp
        self.data.nameToEvent[self.data.counter].price = params.price
        self.data.nameToEvent[self.data.counter].name = params.name
        

    @sp.entry_point
    def addDonation(self, params):
        coin = params.money // 3
        sp.send(params.dest, sp.utils.nat_to_tez(coin), message = "Failed")
        self.data.nameToEvent[params.ids].price = self.data.nameToEvent[params.ids].price - sp.to_int(params.money)
        sp.if self.data.nameToEvent[params.ids].price <= 0:
            self.data.nameToEvent[params.ids].comp = True


    def checkEvent(self, ids):
        sp.if ~(self.data.nameToEvent.contains(ids)):
            self.data.nameToEvent[ids] = sp.record(cause = "", name = "", comp = False, price = 0)

@sp.add_test(name = "AdvancedTest")
def test():
    scenario = sp.test_scenario()

    scenario.h1("Event Planner")
    
    # test addresses
    firstOwner = sp.address("tz1-firstOwner-address-1234")
    secondOwner = sp.address("tz1-firstOwner-address-5678")
    
    # Initiate
    c1 = EventPlanner(firstOwner)
    
    # Print contract instance to HTML
    scenario += c1
    
    scenario.h2("ADD Detail of NGO")
    scenario += c1.setAll(name = "Organisation", cause = "Orphans", comp = False, price = 20).run(sender = firstOwner)
    
    scenario.h2("Want to Donate to this Organisation")
    scenario += c1.addDonation(ids = 1, money = 10, dest = firstOwner).run(sender = secondOwner)
    scenario.h2("Want to Donate to this Organisation")
    scenario += c1.addDonation(ids = 1, money = 10, dest = firstOwner).run(sender = secondOwner)
    
    
    scenario.h2("ADD Detail of NGO")
    scenario += c1.setAll(name = "Organisation2", cause = "Cancer", comp = False, price = 20).run(sender = firstOwner)
    
