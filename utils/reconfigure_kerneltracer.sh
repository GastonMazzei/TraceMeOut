
while IFS= read -r line; do
	echo "$line" > /sys/kernel/debug/tracing/trace_options
done < utils/trace_options.backup
