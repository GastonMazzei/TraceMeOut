
# Backup configuration and activate sys/kernel collection
sudo cp /sys/kernel/debug/tracing/trace_options utils/trace_options.backup
sudo su -c utils/configure_kerneltracer.sh
sudo su -c utils/activate_kerneltracer.sh

# Pipe the kernel trace while collecting user's tags via a python script
(
sudo su -c utils/pipe_kerneltracer.sh &
echo "LASTPID=$!" > utils/lastpid.temp ;
python3 pythonscripts/time_fetcher.py;
)


# Remove the pipe and stop the kernel tracer
source utils/lastpid.temp
kill $LASTPID
sudo  su -c utils/deactivate_kerneltracer.sh

# End
echo "End of the script! :-)"
