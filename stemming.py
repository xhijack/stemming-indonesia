"""
Frequent Term Extraction
Author: Ramdani
Description: Stemming bahasa indonesia
Email: ramdani@sopwer.net
Date: 8 Januari 2015
"""

from kamus import Kamus
from tokenization import cleaning
from tokenization import sentence_extraction
from tokenization import tokenisasi_kalimat
import pdb

inflection_suffixes = ["ku", "mu", "nya"]
particles = ["lah", "kah", "tah", "pun"]
derivation_suffixes = ["i", "an", "kan"]
derivation_prefix = ["di","ke","se","me","be","pe", "te"]
forbidden_prefix = [['be','i'],["di","an"],["ke",["i","kan"]],["me","an"],["se",["i","kan"]],["te","an"]]
kamus = Kamus("kamus.txt")
VOKAL = ['a','i','e','o','u']

class Stem:
    def __init__(self, filename):
        self.filename = filename
        self.results = []

    def __d_suffixes_a(self, kata):
#        print kata
        #cek jika huruf terakhir nya K
        if kata[-1:] == 'k':
            result1 = kata[:-1]
            result = kamus.find(result1)
            if result == False:
                return result1
            else:
                kata = result

        return kata

    def __d_suffixes(self, kata):
        for ds in derivation_suffixes:
            if ds == kata[-len(ds):]:
                kata = kata[:-len(ds)]
                result = kamus.find(kata)
                if result == False:
                    #jika an telah dihapus dan huruf terakhir adalah K maka huruf K dihapus
                    if ds == 'an':
                        #hapus huruf K
                        kata = self.__d_suffixes_a(kata)
                else:
                    #jika ada maka algoritma selesai
                    kata = result
#            else:
#                pass

        return kata
    
    def __particles(self, kata):
        
        for p in particles:
            c = len(p)
            if p == kata[-c:]:
                kata = kata[:-c]
        return kata

    def __i_suffixes(self, kata):

        for ins in inflection_suffixes:
            c = len(ins)
            if ins == kata[-c:]:
                #kalimat yang berujung i suffixes
                kata = kata[:-c]
                result = kamus.find(kata)
                if result == False:
                    pass
                else:
                    kata = result
        return kata
    
    def __d_prefix_a1(self,kata):
            if kata[:2] == 'be' and kata[-1:] == 'i':
                return False
            if kata[:2] == 'di' and kata[-2:] == 'an':
                return False
            if kata[:2] == 'ke' and (kata[-1:] == 'i' or kata[-3:]=='kan'):
                return False
            if kata[:2] == 'me' and kata[-2:] == 'an':
                return False
            if kata[:2] == 'se' and (kata[-1:] == 'i' or kata[-3:]=='kan'):
                return False
            if kata[:2] == 'te' and kata[-2:] == 'an':
                return False

    def __d_prefix_b(self,kata):
        #tentukan jenis awalan
        if kata[:2] == 'di' or kata[:2] == 'ke' or kata[:2] == 'se':
            kata = kata[2:]
        elif kata[:2] == 'te' or kata[:2] == 'be' or kata[:2] == 'me' or kata[:2] == 'pe':
            if kata[:2] == 'te':
                kata = kata[3:]
            elif kata[:2] == 'me' and (kata[:2] == 'l' or kata[:2] == 'r' or kata[:2] == 'w' or kata[:2] == 'y'):
                kata = kata[2:]
            elif kata[:3] == 'mem' and (kata[3] == 'b' or kata[3] == 'r' or kata[3] == 'v' or kata[3] == 'p'):
                kata = kata[3:]
            elif kata[:4] == 'meng' and (kata[4] == 'g' or kata[4] == 'h' or kata[4] == 'q' or kata[4] == 'k'):
                kata = kata[4:]
            elif kata[:4] == 'meng' and (kata[4] in VOKAL):
                kata = "k"+kata[4:]
            else:
                pass
#                print kata
        else:
            pass
        
        return kata

    def __d_prefix_a(self,kata):

        for i in range(0,2):
            if self.__d_prefix_a1(kata) == False:
                break

        return kata

    def __stem(self, kata):
        if len(kata) >= 3:
            result = kamus.find(kata)
            if result == False:
                kata = self.__particles(kata)
                result = kamus.find(kata)
                if result == False:
                    kata = self.__i_suffixes(kata)
#                    print "-->%s" % kata
                else:
                    kata = result
            else:
                kata = result
        
            if type(kata) != list:
                kata = self.__d_suffixes(kata)
                if type(kata) != list:
                    #hilangkan derivation prefix
                    kata = self.__d_prefix_a(kata)
                    kata = self.__d_prefix_b(kata)

        return kata

    def read(self):
        t = open(self.filename)

        text = t.read()
        out = sentence_extraction(cleaning(text))
        #print out[0]
        
        found = 0
        katas = None
        for o in out:
            kalimat = tokenisasi_kalimat(o)
#            print kalimat
            for kata in kalimat:
                #kata = kata.lower()
                result = kamus.find(kata)
                if result == False:
                    index_ = kalimat.index(kata)
                    katas = self.__stem(kata)
                    kalimat[index_] = katas
                else:
                    kalimat[kalimat.index(kata)] = result
                    self.results.append(result)
                    found = found + 1


            print kalimat
#        print self.results
#        print "root word ada %s" % found

if __name__ == "__main__":
    s = Stem("viva.txt")
    s.read()
