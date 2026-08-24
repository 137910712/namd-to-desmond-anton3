import sys
import optparse
from vmd import molecule, atomsel, evaltcl, topology

def parse_cmdline(cmdlineArgs):
    parser = optparse.OptionParser("Usage: python convertNAMDtoDMS.py [options]")
    parser.add_option("-p", "--psffile", action="store", dest="psfFile")
    parser.add_option("-c", "--coorfile", action="store", dest="coorFile")
    parser.add_option("-v", "--velfile", action="store", dest="velFile")
    parser.add_option("-x", "--xscfile", action="store", dest="xscFile")
    parser.add_option("-o", "--outputfile", action="store", dest="outFile")
    parser.add_option("-s", "--centerSystem", action="store_true", dest="doCenter")
    parser.add_option("-S", "--centerSelection", action="store", dest="centerSel")
    parser.set_defaults(doCenter = False, centerSel = "all")

    opts, args = parser.parse_args(cmdlineArgs)
    if (opts.psfFile == None) or (opts.coorFile == None) or (opts.velFile == None) \
       or (opts.xscFile == None) or (opts.outFile == None):
        parser.print_help()
        sys.exit(1)
    return opts.psfFile, opts.coorFile, opts.velFile, opts.xscFile, opts.outFile, opts.doCenter, opts.centerSel

def load_velocities(psfFile, velFile):
    molid = molecule.load("psf", psfFile)
    molecule.read(molid, "namdbin", velFile)
    allVelocities = atomsel("all", molid=molid)
    
    xVel = allVelocities.x
    yVel = allVelocities.y
    zVel = allVelocities.z

    convFactor = 20.4582651391
    xVel = [v * convFactor for v in xVel]
    yVel = [v * convFactor for v in yVel]
    zVel = [v * convFactor for v in zVel]

    molecule.delete(molid)
    return xVel, yVel, zVel

def load_system(psfFile, coorFile):
    molid = molecule.load("psf", psfFile)
    molecule.read(molid, "namdbin", coorFile)
    return molid

def set_velocities(molid, xVel, yVel, zVel):
    allAtoms = atomsel("all", molid=molid)
    allAtoms.vx = xVel
    allAtoms.vy = yVel
    allAtoms.vz = zVel

def save_mol_as_dms(molid, fileName):
    molecule.write(molid, "dms", fileName + ".dms")

def set_pbc(xscFile):
    with open(xscFile, "r") as f:
        for line in f:
            continue 
    items = line.split()
    pbcCommand = f"package require pbctools; pbc set {{ {items[1]} {items[5]} {items[9]} }}"
    evaltcl(pbcCommand)

def center_system(selection, molid):
    centerSel = atomsel(selection, molid=molid)
    negCenter = [-1.0 * item for item in centerSel.center()]
    moveSel = atomsel("all", molid=molid)
    moveSel.moveby(negCenter)

def remove_tip3p_hh_bond(molid):
    h1Sel  = atomsel("resname TIP3 and name H1", molid=molid)
    h2Sel  = atomsel("resname TIP3 and name H2", molid=molid)
    for h1, h2 in zip(h1Sel.index, h2Sel.index):
        topology.delbond(h1, h2, molid=molid)

if __name__ == "__main__":
    psfFile, coorFile, velFile, xscFile, outfile, doCenter, centerSel = parse_cmdline(sys.argv[1:])
    vx, vy, vz = load_velocities(psfFile, velFile)
    molid = load_system(psfFile, coorFile)

    if doCenter:
        center_system(centerSel, molid)

    set_velocities(molid, vx, vy, vz)
    set_pbc(xscFile)
    remove_tip3p_hh_bond(molid)
    save_mol_as_dms(molid, outfile)
    sys.exit(0)
