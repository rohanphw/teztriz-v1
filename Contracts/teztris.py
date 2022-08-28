import smartpy as sp

class Error_message:
    def adminOnly(self):
        return "ADMIN_ONLY"
    
    def invalidPrice(self):
        return "INVALID_PRICE"
    
    def invalidNoOfPlayers(self):
        return "INVALID_NO_OF_PLAYERS"
    
    def invalidMatch(self):
        return "INVALID_MATCH"
    
    def invalidTimePeriod(self):
        return "INVALID_TIME_PERIOD"
    


class teztris(sp.Contract):
    def __init__(self, admin):
        self.error = Error_message()
        
        self.init(
            matchId=sp.nat(0),
            admin = admin,
            matchIds = sp.big_map(tkey = sp.TAddress, tvalue= sp.TNat),
            matches= sp.big_map({}, tkey = sp.TAddress, 
                tvalue = sp.TMap(sp.TNat, sp.TRecord(
                    createdAt= sp.TTimestamp,
                    matchType = sp.TMap(
                            sp.TNat, sp.TRecord(
                                matchDuration= sp.TInt,
                                waitingPeriod = sp.TInt, #to be predefined
                                entryFees = sp.mutez(1000000),
                                minPlayers = sp.TNat(1),
                                maxPlayers = sp.TNat(),
                            )
                        )
                    ),
                    players = sp.TMap(
                        sp.TAddress, sp.TRecord(
                            totalScore = sp.TNat
                        )
                    )
                )
            ),
            ranks = sp.big_map({},
                tkey = sp.TAddress,
                tvalue = sp.TMap(
                    sp.TNat, sp.TMap(
                        sp.TAddress, sp.TNat
                    )
                )
        )
    )
    
#Utility Functions

def _onlyAdmin(self):
    sp.verify(sp.sender == self.data.admin, self.error.adminOnly())

def _matchExists(self, matchId):
    sp.verify(self.data.matchIds.contains(matchId), self.error.matchExists())

def _calculateRanks(self,params):
    sp.set_type(params, sp.TRecord(
        match= sp.TAddress, matchId= sp.TNat,
    ))
    players = sp.local('players', sp.map({}, tkey= sp.TNat, tvalue= sp.TRecord(
        player= sp.TAddress, score= sp.TNat
    )))
    allPlayers= self.data.matches[params.match][params.matchId].players
    index = sp.local('index',0)
    sp.for i in allPlayers.keys():
        players.value[index.value] = sp.record(player= i, score= allPlayers[i].totalScore)
        index.value += 1
    
    sp.for idx in players.value.keys():
        minIdx= sp.local('minIdx', idx)
        sp.for j in sp.range(idx+1, sp.len(players.value.keys())):
            sp.if players.value[j].score > players.value[minIdx.value].score:
                minIdx.value = j

        tempVal= sp.local('tempVal', players.value[idx])
        players.value[idx] = players.value[minIdx.value]
        players.value[minIdx.value] = tempVal.value

    currMatch= sp.local('currMatch', self.data.matches[params.match][params.matchId])
    currScore= sp.local('currScore', 0)
    currPlayers= sp.local('currPlayers', sp.list([], t= sp.TAddress))
    prizePool= sp.utils.mutez_to_nat(currMatch.value.entryFees)*sp.len(allPlayers.keys())
    prizeSum= sp.local('prizeSum', sp.nat(0))
    totalPrize= sp.local('totalPrize', sp.nat(0))

    sp.for i in players.value.keys():
        sp.if players.value[i].score == currScore.value:
            currPlayers.value.push(players.value[i].player)
            prizeSum.value += (prizePool)//1000
            totalPrize.value += (prizePool)//1000
        sp.else:
            sp.if ~self.data.ranks.contains(params.match):
                self.data.ranks[params.match] = sp.map({})
            sp.if ~self.data.ranks[params.match].contains(params.matchId):
                self.data.ranks[params.match][params.matchId] = sp.map({})
            sp.for j in currPlayers.value:
                self.data.ranks[params.match][params.matchId][j] = sp.utils.nat_to_mutez(prizeSum.value/sp.len(currPlayers.value))

            currPlayers.value = sp.list([players.value[i].player])
            currScore.value = players.value[i].score
            prizeSum.value = (prizePool)//1000
            totalPrize.value += (prizePool)//1000
        
    sp.for j in currPlayers.value:
        self.data.ranks[params.match][params.matchId][j] = sp.utils.nat_to_mutez(prizeSum.value/sp.len(currPlayers.value))


#Core Functions
@sp.entry_point
def setAdmin(self, params):
    self._onlyAdmin()
    sp.set_type(params, sp.TAddress)
    self.data.admin = params

@sp.entry_point
def createMatch(self, params):
    sp.set_type(params, sp.TRecord(
        match= sp.TAddress, matchType = sp.TNat
    ))
    sp.if ~self.data.matches.contains(params.match):
        self.data.matches[params.match]= sp.map({},
            tkey= sp.TNat, tvalue= sp.TRecord(
                matchType= sp.TNat,
                createdAt= sp.TTimestamp,
                matchDuration= sp.TInt,
                waitingPeriod = sp.TInt,
                players = sp.TMap(
                    totalScore = sp.TNat
                )
            )
        )
        self.data.matches[params.match][self.data.matchIds[params.match]] = sp.record(
            matchType= params.matchType,
            createdAt = sp.now,
            players = sp.map({},
                tkey= sp.TAddress, tvalue= sp.TRecord(totalScore = sp.TNat)
        )
    )
    self.data.matchIds[params.match] += 1

@sp.entry_point
def joinMatch(self, params):
    sp.set_type(params, sp.TRecord(
        match = sp.TAddress, matchId = sp.TNat
    ))
    self._matchExists(params.matchId)
    newMatch= sp.local('newMatch', self.data.matches[params.match][params.matchId])
    sp.verify(sp.len(newMatch.data.players) <= newMatch.data.matchType.maxPlayers, self.error.invalidNoOfPlayers())
    sp.verify(newMatch.value.createdAt.add_seconds(newMatch.value.matchType.waitingPeriod) > sp.now, self.error.invalidTimePeriod())
    sp.verify(sp.amount == newMatch.value.matchType.entryFees, self.error.invalidPrice())
    sp.verify(newMatch.data.players.contains(sp.sender) == True, self.error.invalidMatch())
    
    self.data.matches[params.matchId].players[sp.source] = sp.record(
        totalScore = 0
    )

@sp.entry_point
def claimExpiredMatch(self, params):
    sp.set_type(params, sp.TRecord(
        match = sp.TAddress, matchId = sp.TNat
    ))
    self._matchExists(params.matchId)
    newMatch= sp.local('newMatch', self.data.matches[params.match][params.matchId])
    sp.verify(newMatch.value.createdAt.add_seconds(newMatch.value.matchType.waitingPeriod) < sp.now, self.error.invalidTimePeriod())
    sp.verify(newMatch.data.players.contains(sp.source), self.error.invalidMatch())
    del self.data.matches[params.matchId].players[sp.source]
    sp.send(sp.source, newMatch.value.matchType.entryFees)

@sp.entry_point
def playMatch(self, params):
    sp.set_type(params, sp.TRecord(
        match = sp.TAddress, matchId = sp.TNat
    ))
    self._matchExists(params.matchId)
    newMatch= sp.local('newMatch', self.data.matches[params.match][params.matchId])
    sp.verify(newMatch.value.createdAt.add_seconds(newMatch.value.matchType.waitingPeriod + newMatch.value.matchType.matchDuration) > sp.now, self.error.invalidTimePeriod())
    sp.verify(newMatch.value.createdAt.add_seconds(newMatch.value.matchType.waitingPeriod) < sp.now, self.error.invalidTimePeriod())
    sp.verify((newMatch.value.players.contains(params.player)), self.error.invalidLeague())

    self.data.matches[params.matchId].players[params.player].totalScore = self.data.matches[params.matchId].players[params.player].totalScore

@sp.entry_point
def claimMatch(self, params):
    sp.set_type(params, sp.TRecord(
        match = sp.TAddress, matchId = sp.TNat
    ))
    self._matchExists(params.matchId)
    newMatch= sp.local('newMatch', self.data.matches[params.match][params.matchId])
    sp.verify(newMatch.value.createdAt.add_seconds(newMatch.value.matchType.waitingPeriod + newMatch.value.matchType.matchDuration) < sp.now, self.error.invalidTimePeriod())

    sp.if ~self.data.ranks.contains(params.match) | ~self.data.ranks[params.match].contains(params.matchId):
        self._calculateRanks(sp.record(match = params.match, matchId = params.matchId))
    
    amount = sp.local('amount', self.data.ranks[params.match][params.matchId].get(sp.sender, sp.mutez(0)))
    self.data.ranks[params.match][params.matchId][sp.source] = sp.mutez(0)

    sp.send(sp.source, amount)