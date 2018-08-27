rm result
pkill python
python3 listener_results.py > /dev/null &
disown
while :
do
    python3 listener_jobs.py > /dev/null
    echo "Job listener failed, restarting in 10 seconds"
    sleep 10
done