import es
import time
import vecmath

# CONFIGS START
## How many times a user can double jump. Resets when he lands. (0 = None, -1 = infinite)
Max_Uses                = 20
## How hard to push the user
Push_Value              = 325
## Minimum time between each jump. (In seconds)
Intervals               = 0.10
## How much extra boost he gets from his falling speed.
## Ex:
#### If this is set to 1  , the push he will get is: (Push_Value + (falling_speed * 1))
#### If this is set to 0.5, the push he will get is: (Push_Value + (falling_speed * 0.5))
#### If this is set to 2  , the push he will get is: (Push_Value + (falling_speed * 2))
#### If this is set to 0  , the push he will get is: (Push_Value + (falling_speed * 0)) (Just Push_Value)
Extra_Boost_If_Falling  = 1

# CONFIGS END

JumpsUsed           = {}
JumpsUsed['count']  = {}
JumpsUsed['time']   = {}
VersionN = "1.4CheeTaH-Public"
VersionD = "1st June 2011"
VersionT = "00:27"
VersionZ = "GMT + 1"

def load():
    es.msg("#multi","\x05[CDJ] #greenCheeTaHs Double Jump #defaulthas been loaded! (#lightgreen%s#default)"%VersionN)
    Set_Up_Public_Var()

def unload():
    es.msg("#multi","\x05[CDJ] #greenCheeTaHs Double Jump #defaulthas been unloaded! (#lightgreen%s#default)"%VersionN)

def es_map_start(ev):
    Set_Up_Public_Var()

def player_say(ev):
    if ev['text'].lower() == '!cdj':
        es.tell(ev['userid'],'CheeTaHs Double Jump:\n%s\n%s\n%s\n%s' %(VersionN,VersionD,VersionT,VersionZ))

def player_jump(ev):
    userid = ev['userid']
    JumpsUsed['count'][userid] = 0
    JumpsUsed['time'][userid] = 0

def Set_Up_Public_Var():
    PubVar = es.ServerVar("cdj_version",VersionN,"Script Version")
    PubVar.set(VersionN)
    PubVar.makepublic()

def client_keypress(ev):
    if not int(ev['status']):
        return
    if ev['keyname'] != 'jump':
        return
    DoTheJump(ev['userid'])

def sm2es_keypress(ev):
    if not int(ev['status']):
        return
    if ev['command'] != 'IN_JUMP':
        return
    DoTheJump(ev['userid'])

def DoTheJump(userid):
    if es.getplayerprop(userid, 'CBasePlayer.pl.deadflag'):
        return
    if userid not in JumpsUsed['time'] or userid not in JumpsUsed['count']:
        ev = {}
        ev['userid'] = userid
        player_jump(ev)
        return
    if JumpsUsed['count'][userid] > Max_Uses and Max_Uses != -1:
        return
    newTime = time.time()
    timeBetween = newTime - JumpsUsed['time'][userid]
    if timeBetween > Intervals:
        if JumpsUsed['count'][userid] > 0:
            Push_Value2 = Push_Value
            if int(es.getplayerprop(userid, 'CBasePlayer.localdata.m_vecVelocity[2]')) < 0:
                Push_Value2 += (round(vecmath.vector((float(es.getplayerprop(userid, 'CBasePlayer.localdata.m_vecVelocity[0]')), float(es.getplayerprop(userid, 'CBasePlayer.localdata.m_vecVelocity[1]')), float(es.getplayerprop(userid, 'CBasePlayer.localdata.m_vecVelocity[2]')))).length(), 2) * Extra_Boost_If_Falling)
            es.setplayerprop(userid,"CBasePlayer.localdata.m_vecBaseVelocity", "0,0,%s" %Push_Value2)
        JumpsUsed['time'][userid] = newTime
        JumpsUsed['count'][userid] += 1