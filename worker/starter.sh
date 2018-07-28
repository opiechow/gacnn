rm result
pkill python
python3 listener_results.py > /dev/null &
disown
python3 listener_jobs.py > /dev/null &
disown