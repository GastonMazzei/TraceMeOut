
# Activate sys/kernel collection
sudo cp /sys/kernel/debug/tracing/trace_options utils/trace_options.backup
sudo mv utils/our_trace_options /sys/kernel/debug/tracing/trace_options
sudo echo "function_graph" > /sys/kernel/debug/tracing/current_tracer

# Spawn a shell with python
python3 pythonscripts/time_fetcher.py

# Store the results
sudo cp /sys/kernel/debug/tracing/trace raw_data/trace

# Restore defaults
sudo echo "nop" > /sys/kernel/debug/tracing/current_tracer
sudo cp utils/trace_options.backup /sys/kernel/debug/tracing/trace_options
