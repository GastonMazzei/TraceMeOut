
# Backup configuration and activate sys/kernel collection
sudo cp /sys/kernel/debug/tracing/trace_options utils/trace_options.backup
sudo su -c utils/configure_kerneltracer.sh
sudo su -c utils/activate_kerneltracer.sh

# Spawn a shell with python
python3 pythonscripts/time_fetcher.py

# Store the results
sudo cp /sys/kernel/debug/tracing/trace raw_data/trace

# Deactivate tracer and restore defaults
sudo  su -c utils/deactivate_kerneltracer.sh

# Let the trace defaults restore themselves and destroy the backup :-)
#sudo su -c utils/reconfigure_kerneltracer.sh
rm utils/trace_options.backup
