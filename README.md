# Implementing BPF in Git with Python

Inspiration from [https://www.acquia.com/blog/pragmatic-guide-branch-feature-git-branching-strategy](https://www.acquia.com/blog/pragmatic-guide-branch-feature-git-branching-strategy).

## Setup

### Set up shared rerere cache
1. Navigate to **cmd**. 
2. Right-click and select "Run as Administrator."
3. Run the command `mkdir \D <path to .git subdirectory of repo>/rr-cache <path to shared rerere cache>`
	- For example, after navigating to the .git subdirectory, I ran the command `mkdir \D rr-cache \\corpnet\cloud\WAL.Live\LIOX.DEV.VSI\Rerere`
4. In the terminal, edit your git configuration with the commands
`git config --global rerere.enabled true` and `git config --global rerere.autoupdate true`

### Set up automated QA branch creation
1. Download the latest version of Python for Windows: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
2. Change the Path variable in Advanced System Properties by appending C:\Scripts\;C:\; to the beginning.
3. Reboot your machine for the Path variable to change.
2. Save the *newqa.py* script in a "Scripts" folder on your C: drive.
3. Incorporate the aliases in config.txt into your .gitconfig file.
4. Save the *qafeatures.txt* file to your Desktop (will work on making location changeable).



## Git commands

`git fstart <feature_name>`

  * This commands starts the creation of a feature by updating the master branch and creating a new feature branch with the supplied name.

`git newqa`

  * This creates a new QA branch out of the features listed in the qafeatures.txt file. Features can be excluded by adding "-x " to the beginning. See qafeatures.txt for an example.

`git imerge <feature_name>`

  * This command checks out the integration branch and merges in the supplied feature.

`git ipush`

  * This command pushes the integration branch to origin.

`git qapush`

  * This command pushes the qa branch to origin. 


## Example workflow 
Elements from [https://www.acquia.com/blog/pragmatic-guide-branch-feature-git-branching-strategy](https://www.acquia.com/blog/pragmatic-guide-branch-feature-git-branching-strategy)
	
	git fstart feature1 // Start a feature called "feature1"
	// Hack hack hack
	git commit -am "My first commit on my feature branch"
	git imerge feature1 // Gets latest integration branch and merges in my feature
	// Resolve any conflicts that arise
	git ipush
	// Hack hack hack and repeat merges to integration
	// Feature is ready for code review, submit pull request, get feedback etc.
	// Now my feature is ready for QA
	// Make sure desired features are indicated in qafeatures.txt
	git newqa // Recreate qa branch
	git qapush // Push qa branch
	git push origin feature1 // Push feature
