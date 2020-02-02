
def escape_team_names(mystr):
    """
    temporary fix for solving ? characters in bad team names encoding
    from LFP's ICS calendar
    """

    mystr = mystr.replace('N?MES','NÎMES')
    mystr = mystr.replace('SAINT-?TIENNE','SAINT-ÉTIENNE')
    mystr = mystr.replace('H?RAULT', 'HÉRAULT')

    return mystr