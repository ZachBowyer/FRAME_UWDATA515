"""
This python file makes sure everything is properly installed and downloaded
Before you run this file, every needed dependency and python should be installed on your local machine
You can do this with Anaconda. conda env create --name FRAME --file=environment.yml
"""
from uszipcode import SearchEngine

#Automatically download zipcode data to your machine
search = SearchEngine(simple_or_comprehensive=SearchEngine.SimpleOrComprehensiveArgEnum.comprehensive)
zipcode = search.by_zipcode(99338)

#Run all unit tests, if they all pass/run then the software has to be correctly installed
#WIP

"""
Information for manually creating/loading anaconda environment from WINDOWS
There is a broken export issue which requires a manual fix 
"""
#Making environment from scratch
# conda remove --name FRAME_windows --all
# conda create --name FRAME_windows python=3.9.0
# conda activate FRAME_windows
# pip install googlemaps
# pip install folium
# pip install polyline
# pip install uszipcode

#Export environemnt
# conda env export > environment.yml
# conda env export --from-history
# conda env export --no-build > environment.yml

#Broken export fix:
# https://github.com/conda/conda/issues/9624
# Opened powershell
# Navigate to c:\Users\<user>\Anaconda3\envs\<env name>\Lib\site-packages\
# Get-ChildItem -File -Recurse -Filter METADATA | Select-String "1.4.1<2.0.0" | Select-Object -Unique Path
# C:\Users\Zach\anaconda3\envs\FRAME_windows\Lib\site-packages\sqlalchemy_mate-1.4.28.3.dist-info\METADATA
# Requires-Dist: sqlalchemy (>=1.4.1<2.0.0) to Requires-Dist: sqlalchemy (>=1.4.1,<2.0.0)

# Delete environment
# conda deactivate
# conda remove --name FRAME_windows --all

# Install environment from yml file
# conda env create --name FRAME_windows --file=environment.yml
# conda info --envs (See if it exists)
# conda activate FRAME_windows

"""
LINUX
"""
#Making environment from scratch
# conda remove --name FRAME_linux --all
# conda create --name FRAME_linux python=3.9.0
# pip install googlemaps
# pip install folium
# pip install polyline
# pip install uszipcode

#Export environment
# conda env export > environment_linux.yml

#Broken export fix
#Navigate to ~/miniconda3/envs/FRAME_linux/lib/python3.9/site-packages/sqlalchemy_mate-1.4.28.3.dist-info/METADATA
#vi METADATA
#Change Requires-Dist: sqlalchemy (>=1.4.1<2.0.0) to Requires-Dist: sqlalchemy (>=1.4.1,<2.0.0)