#2/20/17: This code should be close to working (or work) with the draftkings API.
# It's from the lineup picks file in the old NBA files. There is a lot of good stuff in there, the first half is basically all predictions, and the second half is evaluating the best lineup and stuff vs. what actually happened.
#Should be able to scavenge a good deal of code in there to be reused.


class SetOfPlayers:
    '''Takes in '''
    def key1(self, a):
        return(a.salary, -a.dkpoints)

    def getValidPlayers(self,players,num=3):
        tmp1=[0] * num
        players.sort(key=self.key1)
        counter=0
        while counter < len(players):
            tmp1.sort(reverse=True)
            player = players[counter]
            if player.dkpoints <= tmp1[-1]:
                players.remove(player)
                continue
            tmp1.pop()
            tmp1.append(player.dkpoints)
            counter += 1
        return players

    def __init__(self, players):
        players.sort()
        self.bestVal = players[0].dkpoints / players[0].salary
        self.pgs=self.getValidPlayers([x for x in players if x.pos == 'PG' and x.dkpoints > 0])
        self.sgs=self.getValidPlayers([x for x in players if x.pos == 'SG' and x.dkpoints > 0])
        self.gs=self.getValidPlayers( self.sgs + self.pgs )
        self.pfs=self.getValidPlayers([x for x in players if x.pos == 'PF' and x.dkpoints > 0])
        self.sfs=self.getValidPlayers([x for x in players if x.pos == 'SF' and x.dkpoints > 0])
        self.fs=self.getValidPlayers( self.pfs + self.sfs )
        self.cs=self.getValidPlayers([x for x in players if x.pos == 'C' and x.dkpoints > 0], 2)
        self.uts=self.getValidPlayers( self.gs + self.fs + self.cs )

    def notGoingToWork(self, team, bestTeam):
        if team.getNumRemainingPlayers() * 3000 > team.getRemainingBudget():
            return True
        if team.getRemainingBudget() * self.bestVal + team.getScore() < bestTeam.getScore():
            return True
        return False

    def getPerms(self):

        return len(self.pgs) * len(self.sgs) * len(self.gs) * len(self.sfs) * len(self.pfs) * len(self.cs)* len(self.fs) * len(self.uts)

    def getStats(self):
        #TODO: I added this logic to fix it when it divides by zero. Not sure if this was the right way to do this, so check it out later.
        if self.getPerms() == 0:
            return (self.bestTeam.getScore(), self.tries, self.getPerms(), float(self.tries) / 1, len(self.improvements), self.improvements)
        return (self.bestTeam.getScore(), self.tries, self.getPerms(), float(self.tries) / self.getPerms(), len(self.improvements), self.improvements)

    def findBest(self):
        self.pgs.sort()
        self.sgs.sort()
        self.gs.sort()
        self.pfs.sort()
        self.sfs.sort()
        self.cs.sort()
        self.fs.sort()
        self.uts.sort()
        self.bestTeam = dkTeam()
        self.tries = 0
        self.improvements = []
        for pg in self.pgs:
            team = dkTeam()
            team.removePF()
            if not team.addPG(pg) or self.notGoingToWork(team, self.bestTeam):
                team.removePG()
                continue
            for sg in self.sgs:
                if not team.addSG(sg) or self.notGoingToWork(team, self.bestTeam):
                    team.removeSG()
                    continue
                for g in self.gs:
                    if not team.addG(g) or self.notGoingToWork(team, self.bestTeam):
                        team.removeG()
                        continue
                    for pf in self.pfs:
                        if not team.addPF(pf) or self.notGoingToWork(team, self.bestTeam):
                            team.removePF()
                            continue
                        for sf in self.sfs:
                            if not team.addSF(sf) or self.notGoingToWork(team, self.bestTeam):
                                team.removeSF()
                                continue
                            for f in self.fs:
                                if not team.addF(f) or self.notGoingToWork(team, self.bestTeam):
                                    team.removeF()
                                    continue
                                for c in self.cs or self.notGoingToWork(team, self.bestTeam):
                                    if not team.addC(c) or self.notGoingToWork(team, self.bestTeam):
                                        team.removeC()
                                        continue
                                    for ut in self.uts:
                                        if not team.addUtil(ut) or self.notGoingToWork(team, self.bestTeam):
                                            team.removeUtil()
                                            continue
                                        self.tries += 1
                                        if team.getScore() > self.bestTeam.getScore() and team.isValidTeam():
                                            self.improvements.append((self.tries, self.bestTeam.getScore()))
                                            self.bestTeam.clearPlayers()
                                            team.copy(self.bestTeam)
                                        team.removeUtil()
                                    team.removeC()
                                team.removeF()
                            team.removeSF()
                        team.removePF()
                    team.removeG()
                team.removeSG()

def doThing(y): # Finds the optimal lineup using the SetOfPlayers class
    ys=[y[x:x+20] for x in range(10)]
    ns=[SetOfPlayers(x) for x in ys]
    for n in ns:
        t1=time.time()
        n.findBest()
        t2=time.time()
        print n.getPerms(), 'NPERMS'
        print len(n.improvements), 'LENNNIMPROVEMENTS'
        print n.improvements, 'NIMPROVEMENTS'
        print n.getStats(), 'GETSTATS'
        if len(n.bestTeam.players) is not 0:
            print [x.name for x in n.bestTeam.players], 'BESTSTATS'
        return [n.bestTeam.getScore(), [x.name for x in n.bestTeam.players]]

        #Uncomment the following code if you want the whole shebang, not just the first lineup's score (which tends to be the highest, #TODO: but you haven't tested as of 2/11/16
        '''
        print n.getPerms(), 'NPERMS'
        print len(n.improvements), 'LENNNIMPROVEMENTS'
        print n.improvements, 'NIMPROVEMENTS'
        print n.getStats(), 'GETSTATS'
        if len(n.bestTeam.players) is not 0:
            print [x.name for x in n.bestTeam.players], 'BESTSTATS'
