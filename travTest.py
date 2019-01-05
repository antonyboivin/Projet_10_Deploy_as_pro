
import os

print(os.getcwd())
os.chdir("./PurBeurre")
print(os.getcwd())
for root, dirs, files in os.walk("."):
  for filename in files:
    print(filename)
