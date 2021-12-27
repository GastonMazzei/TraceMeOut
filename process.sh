
# Clean and Prepare
mkdir processed_trace
rm processed_trace/*
rm *.pkl

# Process Data: build list of times, yaml, and mapping between names and values
python3 pythonscripts/Processor1.py
python3 pythonscripts/Processor2.py

# Build a time-dependent graph-structure according to the Configuration file
python3 pythonscripts/Processor3.py

# Update the configuration file with the correct sizes that  resulted from the building
python3 pythonscripts/Processor4.py

rm processed_trace/*.txt
rm *.log



