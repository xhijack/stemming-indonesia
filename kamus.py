import sys
class Kamus:
	def __init__(self,filename):
		self.filename = filename
	
	def find(self,keyword):
		flag = False
		with open(self.filename) as f:
    			for line in f:
        			word = line.split(" ")[0]
				#print line.split(" ")[1]
				if word.lower() == keyword.lower():
					return (line.split(" "))
					break
				else:
					flag = False
			return False

if __name__ == "__main__":
	argv = sys.argv[1:]
	k = Kamus("kamus.txt")
	print k.find(argv[0])
