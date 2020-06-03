# Flask examples
Run file `run_web.py` using Python 3. You have to provide a port with argument `-p` or `--port` and server type with `-s` or `--server`, see also `python3 run_web.py --help`.

The console will give the address, containing `0.0.0.0:PORT` where `PORT` is your given port. `http://0.0.0.0:PORT/` will give a 404, but see below for URLs you can visit.

Please see the cource code what is happening! Feel free to ask me (Auke) questions regarding this.

## Example template use
Go to `http://0.0.0.0:PORT/test` and try to set some parameters (or no parameters), for example `http://0.0.0.0:PORT/test?param1=test&params2=something` etc.

## Example API use
Only the API GET call for `/api/user/address` for the central server.

Go to `http://0.0.0.0:PORT/api/user/address` and try setting a username as parameter, so like `http://0.0.0.0:PORT/api/user/address?username=someusername`.

