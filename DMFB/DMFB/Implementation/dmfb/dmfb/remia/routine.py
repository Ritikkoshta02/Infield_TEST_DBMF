def insertCheckpoint1X((x,y), t):
#==================================================================================
# A droplet (1X) must appear on (x,y) at t
#==================================================================================
    constraint = ""
    for d in dropletIdList:
        constraint += "If(a_%d_%d_%d_%d == True, 1, 0) + "%(x,y,d,t)
    constraint = constraint[:-2] + "== 1)\n"
    s.add(constraint)
    if cellInDmfb(x, y) == False:
        print 'insertCheckpoint: cell (%d,%d) is not in DMFB'%(x,y)
        return
    else:
        clauseFile.write("#================================================================================================\n")
        clauseFile.write("# Checkpoint (1X) on (%d,%d) at %d \n"%(x,y,t))
        clauseFile.write("#================================================================================================\n")

        constraint = "s.add("
        for d in dropletIdList:
            constraint += "If(a_%d_%d_%d_%d == True, 1, 0) + "%(x,y,d,t)
        constraint = constraint[:-2] + "== 1)\n"
        clauseFile.write(constraint)
