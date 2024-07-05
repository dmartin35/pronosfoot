
def escape_team_names(mystr):
    """
    temporary fix for solving ? characters in bad team names encoding
    from LFP's ICS calendar
    """

    mystr = mystr.replace('N?MES','NÎMES')
    mystr = mystr.replace('SAINT-?TIENNE','SAINT-ÉTIENNE')
    mystr = mystr.replace('H?RAULT', 'HÉRAULT')

    mystr = mystr.replace('N?MES', 'NÎMES')
    mystr = mystr.replace('SAINT-Ã\x89TIENNE', 'SAINT-ÉTIENNE')
    mystr = mystr.replace('HÃ\x89RAULT', 'HÉRAULT')

    return mystr