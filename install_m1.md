## Installation Guide for M1 Macbook
It is possible to install Scenic and gfootball on Macbooks with M1 chip. However, it is not possible (and not a good choice anyway) to install RL components. Please follow the this guide instead of the README. 

First, make sure you upgrade to the latest Mac OS Version.

Second, we must use x86 homebrew (which requires rosetta) to install all dependencies, including Python3 and simulator. Therefore we need to install homebrew for x86, not M1. Notice you must install the **latest** version of everything, as specified by the brew formula, through the x86 homebrew. If you already installed homebrew for M1, it will be easier to uninstall homebrew completely. If you don't want to do that, you will have 2 versions of homebrew on your system, with two different Cellar locations. You must make sure you use the x86 homebrew to install components, and link all project related components in the x86 cellar.

The following guide assumes that you only have the x86 homebrew installed. 
1.  You can install homebrew x86 using: 
```
arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```
2. Make sure you use the following command **every time** to install packages:
```
arch -x86_64 brew install <package>
```
3. Now install the brew dependencies for gFootball simulator. Refer to README for the latest instruction. Remember step 2!!!
```
arch -x86_64 brew install git python3 cmake sdl2 sdl2_image sdl2_ttf sdl2_gfx boost boost-python3
```
After this, you will notice that homebrew installed the latest Python3 for you, and you **must** use this installed Python3. Modify your path variable, or otherwise, so that `python3` points to this installation.

From this step onwards, we assume `python3` points to brew python3 installation. Use `which python3` to double check.

3. Continue the gfootball installation by upgrading pip first.
python3 -m pip install --upgrade pip setuptools psutil wheel

4. Install Poetry and Scenic as instructed in README. Make sure poetry uses the python3 installed by brew. Remember to use poetry shell to activate the virtual environment.

5. If there are issues installing scenic try running: 
```
arch -x86_64 brew install geos
pip install -U shapely -I --force-reinstall --no-cache
```

6. In the poetry virtual environment, do step 3 again and pip install gfootball. Refer to the step 2 at https://github.com/google-research/football#on-your-computer.

7. To verify you have successfully installed gfootball, run the following command to play the game.
```python3 -m gfootball.play_game --action_set=full```




