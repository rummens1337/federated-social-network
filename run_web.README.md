Run file `run_web.py` using Python 3. You have to provide a port with argument `-p` or `--port`, see also `python3 run_web.py --help`.

The console will give the address, containing `0.0.0.0:PORT` where `PORT` is your given port. `http://0.0.0.0:PORT/` will give 404, but go to `http://0.0.0.0:PORT/test` and try to set some parameters (or not parameters), for example `http://0.0.0.0:PORT/test?param1=test&params2=something` etc.

