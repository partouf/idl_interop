import sys

if len(sys.argv) > 1:
    idlfilepath = sys.argv[1]
else:
    print("Please supply .idl filepath")
    exit(1)

outextension = ".pas"

from idl_parser import parser
parser_ = parser.IDLParser()

idlfile = open(idlfilepath, "r")
idl_str = idlfile.read()
idlfile.close()

outfile = 0

def printInterface(interface):
    outfile.write('  %s = interface\n' % (interface.name))
    for m in interface.methods:
        if m.returns.name == 'void':
            outfile.write('    procedure %s(' % m.name)
        else:
            outfile.write('    function %s(' % m.name)

        firstarg = 1
        for a in m.arguments:
            if firstarg:
                firstarg = 0
            else:
                outfile.write("; ")

            if 'out' in a.direction:
                outfile.write('var %s: %s' % (a.name, a.type))
            else:
                outfile.write('const %s: %s' % (a.name, a.type))

        if m.returns.name == 'void':
            outfile.write(');\n')
        else:
            outfile.write('): %s;\n' % m.returns.name)

    outfile.write('  end;\n\n')

def printStruct(struct):
    outfile.write('  %s = record\n' % struct.name)
    for m in struct.members:
        outfile.write('    %s: %s;\n' % (m.name, m.type.name))
    outfile.write('  end;\n\n')

def printTypeDef(typedef):
    outfile.write('  %s = %s;\n\n' % (typedef.name, typedef.type.name))

def printEnum(enum):
    outfile.write('  %s = (\n' % enum.name)
    first = 1
    for v in enum.values:
        if not first:
            outfile.write(',\n')
        else:
            first = 0
        outfile.write('    %s = %s' % (v.name, v.value))
    outfile.write('\n  );\n\n')

def printMod(module):
    global outfile
    outfile = open(module.name + outextension, "w")
    outfile.write('unit %s;\n\n' % module.name)
    outfile.write('interface\n\n')
    outfile.write('uses\n')
    outfile.write('  IDLUtils;\n\n')
    outfile.write('type\n')
    module.for_each_typedef(printTypeDef)
    module.for_each_enum(printEnum)
    module.for_each_struct(printStruct)
    module.for_each_interface(printInterface)
    outfile.write('implementation\n\n')
    outfile.write('end.\n')
    outfile.close()

global_module = parser_.load(idl_str)
global_module.for_each_module(printMod)
