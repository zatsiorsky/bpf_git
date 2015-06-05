# James Zatsiorsky
# 6/04/15
# A script which reads a file of features and creates a new QA branch

# Allows the use of the command line within the script
import subprocess

# For exiting script
import sys

# Array to hold features to QA
features = []

# Open the file containing the features for QA (this file location may change)
f = open('../qafeatures.txt', 'r')

for line in f:
	line = line.split("\n")[0]
	# Check if feature is excluded
	check = line.split(" ")[0]
	if check != "-x":
		features.append(line)
	
# Create a local QA branch off of the last commit in master
# The previous QA branch should be deleted beforehand, or else the command will not run.
result = subprocess.call(["git", "branch", "QA", "master", "-q"])

if result == 0: # successful 
	print ("Successfully created QA branch.\n")
else: # failed
	recreate = input("\nThe QA branch already exists. Recreate branch? (y/n): ")
	if recreate == "y": # Delete the old branch and recreate the QA branch
		print("\n")
		# In case we are currently on QA branch
		subprocess.call("git checkout master --quiet")
		subprocess.call("git branch -D QA")
		# Recreate the QA branch
		subprocess.call(["git", "branch", "QA", "master", "-q"])
	else:	
		print ("Aborting script.\n")
		sys.exit()

# Switch over to new QA branch.
subprocess.call(["git", "checkout", "QA"])

# Merge in each of the features listed.
for feature in features:
	result = subprocess.call(["git", "merge", "--no-ff", feature, "--quiet", "--no-commit"])
	subprocess.call(['git', 'commit', '-am', 'adding feature %s' % feature, '--no-edit'])

	if result == 1: # We have a merge conflict
		# Check if the merge conflict has been resolved by rerere
		output = subprocess.check_output("git rerere status")
		conflicts = output.decode().split("\n")
		if len(conflicts) <= 1: # Conflict fixed by rerere
			print ("\nConflict resolved by rerere")
		else: # There is a conflict that needs to be resolved manually
			print ("\nRerere could not resolve this conflict.\n")
			print ("\n ##### Manually fix the conflict, commit the fix, and run the script again. ##### \n")
			sys.exit()
			
	print ("\n ###### Successfully merged %s. #####\n" % feature)

print (" ###########################################")
print (" #####                                 #####")
print (" ##### QA branch successfully created! #####")
print (" #####                                 #####")
print (" ###########################################\n")