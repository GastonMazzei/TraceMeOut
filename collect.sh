
rm raw_data/trace
rm *.info

echo "function_graph" > /sys/kernel/debug/tracing/current_tracer
echo "funcgraph-abstime" >> /sys/kernel/debug/tracing/trace_options

# Compute the processor's time offset :-)
PER_CPU_BASE=/sys/kernel/debug/tracing/per_cpu
sudo ls $PER_CPU_BASE > temp
while IFS= read -r line; do
	sudo cat "$PER_CPU_BASE/$line/stats" > "$line.info" 
done < temp



# Collect data from user until explicit termination
(
cat /sys/kernel/debug/tracing/trace_pipe >> raw_data/trace &
LASTPID=$! ;
python3 pythonscripts/time_fetcher.py;
kill $LASTPID
)


# Stop Tracer (at leas one should suceed ;-)
echo "nop" > /sys/kernel/debug/tracing/current_tracer
echo "nop" > /sys/kernel/debug/tracing/current_tracer
echo "nop" > /sys/kernel/debug/tracing/current_tracer
echo "nop" > /sys/kernel/debug/tracing/current_tracer
echo "nop" > /sys/kernel/debug/tracing/current_tracer
echo "nop" > /sys/kernel/debug/tracing/current_tracer

# Erase processor's info 
rm *.info

# End
echo "End of the script! :-)"


# Print alert on how to stop the tracer if there was a Ctrl+C kill instead of 'exit' gracefully
echo "More Info:"
echo "If Ctrl+C was sent to Python3, and the CPU remains super busy, it could be that the tracer got jammed ON and it is still being recorded. To fix you can reboot OR: 
'sudo su'
'ps'
'kill (PID of the cat process)'
'echo nop > /sys/kernel/debug/tracing/current_tracer'"
