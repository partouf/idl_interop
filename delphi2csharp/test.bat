@echo off

cd test1

python ../idl2pasintf.py test1.idl
python ../idl2pasdllhandler.py test1.idl
python ../idl2pasimpl2cdll.py test1.idl

python ../idl2csintf.py test1.idl


del *.exe
dcc32 -Q -CC -B -NSSystem;WinAPI test1.dpr
echo ----
del *.dcu
test1.exe

cd ..