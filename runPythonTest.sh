python -m SimpleHTTPServer 8888 &
pid=$!
python python_single.py
kill $pid
