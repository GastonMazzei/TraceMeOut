
rm raw_data/trace

echo "function_graph" > /sys/kernel/debug/tracing/current_tracer
echo "funcgraph-abstime" >> /sys/kernel/debug/tracing/trace_options


# Collect data from user until explicit termination
(
cat /sys/kernel/debug/tracing/trace_pipe >> raw_data/trace &
LASTPID=$! ;
python3 pythonscripts/time_fetcher.py;
kill $LASTPID
)


# Stop Tracer
echo "nop" > /sys/kernel/debug/tracing/current_tracer

# End
echo "End of the script! :-)"


# Print alert on how to stop the tracer if there was a Ctrl+C kill instead of 'exit' gracefully
echo "More Info:"
echo "If Ctrl+C was sent to Python3, and the CPU remains super busy, it could be that the tracer got jammed ON and it is still being recorded. To fix you can reboot OR: 
'sudo su'
'ps'
'kill (PID of the cat process)'
'echo nop > /sys/kernel/debug/tracing/current_tracer'"
