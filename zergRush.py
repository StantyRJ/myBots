from cProfile import run
from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3
from sc2.ids.unit_typeid import UnitTypeId

class STARCRAFT2BOT(BotAI):
    async def on_step(self, iteration: int):

        attackTarget: Point2 = self.enemy_structures.not_flying.random_or(self.enemy_start_locations[0]).position

        #base loop up here try and make drones, zerglings or overlords
        if self.supply_left < 2 and self.already_pending(UnitTypeId.OVERLORD) < 1:
            if self.can_afford(UnitTypeId.OVERLORD):
                self.train(UnitTypeId.OVERLORD)

        
        if self.townhalls:
            hatchery = self.townhalls.random
            if hatchery.is_idle and self.can_afford(UnitTypeId.DRONE) and self.supply_left >= 2 and self.supply_workers < 16:
                self.train(UnitTypeId.DRONE)
        
        #train zerglings
        if self.structures(UnitTypeId.SPAWNINGPOOL).ready and self.larva and self.can_afford(UnitTypeId.ZERGLING) and self.supply_left >= 2:
            _amount_trained: int = self.train(UnitTypeId.ZERGLING, self.larva.amount)

        #make zerglings attack once they spawn
        if self.units(UnitTypeId.ZERGLING).amount >= 16:
            for zergling in self.units(UnitTypeId.ZERGLING):
                zergling.attack(attackTarget)

        #try and build exteras down here 
        #first try and build a spawningpool
        if self.structures(UnitTypeId.SPAWNINGPOOL).amount + self.already_pending(UnitTypeId.SPAWNINGPOOL) == 0:
            if self.can_afford(UnitTypeId.SPAWNINGPOOL):
                await self.build(UnitTypeId.SPAWNINGPOOL, near=hatchery)

        

run_game(
    maps.get("2000AtmospheresAIE"),
    [Bot(Race.Zerg, STARCRAFT2BOT()),
     Computer(Race.Protoss, Difficulty.VeryEasy)],
     realtime = False
)