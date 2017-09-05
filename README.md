# WebSphere Application Server scripts
Useful (at least for me) wsadmin scripts for WebSphere Application Server (7.x, 8.x, 9.x)

These scripts can target one or some or all the servers of a cell if run from the DMGR.
First 3 parameters are :
  * cell (or all)
  * node (or all)
  * server (or all)
  

# Usage
*wsadmin.sh -conntype none -lang jython -f <script_none.py> [parameters]*
(WAS server can be stopped)

or 

*wsadmin.sh -conntype SOAP -lang jython -f <script_soap.py> [parameters]*
(WAS server must be running)
  
# Documentation
Launch a script without any parameter to get help.

# License
This tool is licensed under the [MIT License](LICENSE).

