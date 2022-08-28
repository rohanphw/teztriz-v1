import smartpy as sp

teztris = sp.io.import_stored_contract('teztris')

@sp.add_test(name = 'teztris')
def test():
    scenario = sp.test_scenario()
    scenario.h1('Teztris')

    admin=sp.test_account('admin')
    player1=sp.test_account('player1')
    player2=sp.test_account('player2')
    match1= sp.test_account('match1')

    c = teztris.teztris(admin = admin.address)
    scenario += c

# #-------------Set admin-----------------

# #Should not set admin if not called by the current admin
      c.setAdmin(player1.address).run(sender = player1, valid= False)

# #Should update the admin
      c.setAdmin(player1.address).run(sender = admin)

# #-------------Create match-----------------

# #Should not create match if waiting period, duration min player is 0
      c.createMatch(sp.record(
        matchType= "0", waitingPeriod="3600", matchDuration="0", match = match1.address, maxPlayers="2"
         )).run(sender = admin, valid= False)

# #Should create a match
      c.createMatch(sp.record(
        matchType= "0", waitingPeriod="3600", matchDuration="86400", match = match1.address, maxPlayers="2"
         )).run(sender = admin)

# #-------------Join match--------------------

# #Should not join match if not called by the playe



    