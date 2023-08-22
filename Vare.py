import subprocess
import marshal
import base64
import zlib
import random
import string
import argparse
from cryptography.fernet import Fernet

class VareObfuscator:
    def genjunk():
        return f"""
def saint{random.randint(99999, 9999999)}():
    if {random.randint(99999, 9999999)} == {random.randint(99999, 9999999)}:
    
        print({random.randint(99999, 9999999)})
        aaa{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

        print({random.randint(99999, 9999999)})
        bbb{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

        aa{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

        z{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        zz{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

        c{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        cc{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

    elif {random.randint(99999, 9999999)} == {random.randint(99999, 9999999)}:
    
        print({random.randint(99999, 9999999)})

        aaa{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        print({random.randint(99999, 9999999)})

        bbb{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        aa{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        x{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        xx{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

        a{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        aa{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
    """

    def junkgenerator(junkrange):
        junks = ''
        for a in range(junkrange):
            junks += VareObfuscator.genjunk()
        return junks

    def random(length):
        letters = string.ascii_letters
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string

    def obfuscate(file):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        numeric = lambda _: "|".join(str(ord(__)) for __ in _)[::-1]
        newdataname = VareObfuscator.random(15)
        newkeyname = VareObfuscator.random(15)
        exec1 = '''__x__ = lambda _: "".join(chr(int(__)) for __ in _.split('|'));data1 = __x__(dataname[0][::-1]);data2 = __x__(dataname[1][::-1]);data3 = __x__(dataname[2][::-1]);__vare__(___vare___(data1+data3+data2, keyname))'''.replace('dataname', newdataname).replace('keyname', newkeyname)
        with open(file, encoding='utf-8') as a:
            b = a.read()
        vare = fernet.encrypt(base64.b64encode(zlib.compress(marshal.dumps(compile(b, '<vare>', 'exec'))))).hex()
        splitto = 3
        lengths = len(vare) // splitto
        extra = len(vare) % splitto
        varedata = []
        start = 0
        for i in range(splitto):
            end = start + lengths
            if i < extra:
                end += 1
            varedata.append(vare[start:end])
            start = end
        with open('stub', encoding='utf-8') as x:
            aa = x.read()
            a = aa.replace('%KEY%', key.decode()).replace('%1%', numeric(varedata[0])).replace('%2%', numeric(varedata[2])).replace('%3%', numeric(varedata[1])).replace('%KEY2%', key.decode()).replace('%DATA2%', fernet.encrypt(base64.b64encode(zlib.compress(marshal.dumps(compile(exec1, '<vare>', 'exec'))))).hex()).replace('4545454454545454545454545', VareObfuscator.random(10)).replace('555555555555555555555555', VareObfuscator.random(15)).replace('4444444444444444444444444', VareObfuscator.random(10)).replace('dataname', newdataname).replace('keyname', newkeyname)
        if args.junk:
            a = a.replace('%junk1%', VareObfuscator.junkgenerator(15)).replace('%junk2%', VareObfuscator.junkgenerator(15)).replace('%junk3%', VareObfuscator.junkgenerator(15)).replace('%junk4%', VareObfuscator.junkgenerator(15)).replace('%junk5%', VareObfuscator.junkgenerator(15))
        else:
            a = a.replace('%junk1%', '').replace('%junk2%', '').replace('%junk3%', '').replace('%junk4%', '').replace('%junk5%', '')
        if args.sign:
            with open('Obfuscated.py', 'w', encoding='utf-8') as y:
                y.write("# This Code Obfuscated With 'Vare Obfuscator 2.0'\n"+a)
            subprocess.call('pyinstaller --clean --onefile Obfuscated.py')
            subprocess.call('python sigthief.py -i sign.exe -t ./dist/Obfuscated.exe -o Vare.exe')
        else: 
            with open('Obfuscated.py', 'w', encoding='utf-8') as y:
                y.write("# This Code Obfuscated With 'Vare Obfuscator 2.0'\n"+a)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Vare Obfuscator 2.0")
    parser.add_argument("file", help="Enter the file name containing the Python code to obfuscate")
    parser.add_argument("--junk", action="store_true", help="Inject junk code into the obfuscated code")
    parser.add_argument("--sign", action="store_true", help="Compile your code with PyInstaller and sign it with SigThief (For Low Detection) - If you want to use this option, add the modules of your own code to the top line of the stub file, otherwise it will not work when converted to exe.")
    args = parser.parse_args()
    VareObfuscator.obfuscate(args.file)