# ===========================================
# generate JVM dumps, heap, system, threads
# for one or more servers
# ===========================================
script_name = "jvm_generate_dump_soap.py"

import sys

def print_usage():
  print('\nUsage: wsadmin.sh [-conntype SOAP] -lang jython -f <%s> <cell|all> <node|all> <server|all> <heap:system:thread>' % script_name)
  print
  return

def print_jvms():
  """
    print list of available JVM
  """
  print('\nDefined JVMs are:')
  jvms = AdminConfig.list('JavaVirtualMachine').split( lineSeparator)
  for jvm in jvms:
    cell_node_server = jvm.split('|')[0].split('/')
    _cell = cell_node_server[1]
    _node = cell_node_server[3]
    _serv = cell_node_server[5]
    print('  [ cells / %s / nodes / %s / servers / %s ]' % (_cell, _node, _serv))
  print
  return

def jvm_generate_dump( *argv):
  # list all properties available with this script
  available_props = ['IBM_COREDIR', 'IBM_HEAPDUMP', 'IBM_HEAPDUMPDIR', 'IBM_HEAPDUMP_OUTOFMEMORY',  'IBM_HEAP_DUMP', 'IBM_JAVACOREDIR', 'IBM_JAVADUMP_OUTOFMEMORY', 'IBM_JAVA_HEAPDUMP_TEXT', 'IBM_JAVA_HEAPDUMP_TXT', 'JAVA_DUMPS_OPTS', 'com.ibm.websphere.threadmonitor.interval', 'com.ibm.websphere.threadmonitor.threshold', 'com.ibm.websphere.threadmonitor.false.alarm.threshold', 'com.ibm.websphere.threadmonitor.dump.java', 'com.ibm.websphere.threadmonitor.dump.stack']
  
  # first check if we are really connected: AdminTask should be available
  try:
    cellName = AdminControl.getCell()
  except:
    print('\nWARNING: Not connected')
    print_usage()
    print_jvms()
    # sys.exit()
    return
    
  # test parameter
  print('-'*20)
  if len( argv) == 4: 
    cell = argv[0]
    node = argv[1]
    serv = argv[2]
    mode = argv[3].lower().split(':')
    gen_heap = gen_system = gen_thread = ''
    if 'heap' in mode: gen_heap = 'heap'
    if 'system' in mode: gen_system = 'system'
    if 'thread' in mode: gen_thread = 'thread'
    if (gen_heap != '') or (gen_system != '') or (gen_thread != ''):
      print('Generating [%s:%s:%s] dump for [ cells / %s / nodes / %s / servers / %s ]' % (gen_heap, gen_system, gen_thread, cell, node, serv))
    else:
      print_usage()
      print('\nWARNING: No correct parameter passed to the script...')
    
  if (len( argv) != 4) or (gen_heap+gen_system+gen_thread == ''):
    print_usage()
    print_jvms()
    # sys.exit()
    return
  
  # generate dump GC for selected jvm
  found = 0
  only_application_server = 'true'
  jvms = AdminControl.queryNames('type=JVM,*').split( lineSeparator)
  for jvm in jvms:
    jvmObj = AdminControl.makeObjectName( jvm)
    _cell = jvmObj.getKeyProperty( 'cell')
    _node = jvmObj.getKeyProperty( 'node')
    _serv = jvmObj.getKeyProperty( 'process')
    # retrieve server type
    server_type = jvmObj.getKeyProperty( 'type')
    # if 'all' is used then activate only if server type is APPLICATION_SERVER
    # else if 'all' is not used then user knows what he does so activate even if server type is not APPLICATION_SERVER
    # do if only current jvm is targeted
    if (_cell == cell or cell == 'all') and (_node == node or node == 'all') and (_serv == serv or serv == 'all'):
      print('-'*20)
      print('[ cells / %s / nodes / %s / servers / %s ]' % (_cell, _node, _serv))
      found = found + 1
      print('-'*20)
      if gen_heap == 'heap':
        print "  generating HEAP dump..."
        AdminControl.invoke( jvm, 'generateHeapDump')		# <profile-name>/heapdump.<date>..<timestamp><pid>.phd
      if gen_thread == 'thread':
        print "  generating THREAD dump (javacore)..."
        AdminControl.invoke( jvm, 'dumpThreads')			# <profile-name>/javacore.<date>..<timestamp><pid>
      if gen_system == 'system':
        print "  generating SYSTEM dump..."
        AdminControl.invoke( jvm, 'generateSystemDump')		# <profile-name>/core.<date>..<timestamp><pid>.dmp
      # get server properties for current jvm (to show dump directories)
      print("\n  currents properties of this server:")
      props = AdminConfig.list( 'Property', '(cells/%s/nodes/%s/servers/%s|server.xml)' % (_cell, _node, _serv)).split( lineSeparator)
      # print props
      for p in props:
        if p != '':
          v = {}
          v['name'] = AdminConfig.showAttribute( p, 'name')
          v['value'] = AdminConfig.showAttribute( p, 'value')
          if (v['name'] in available_props):
            print( "    %-30s '%s'" % (v['name'], v['value']))
  
  # display list of jvm available if no match
  if not found:
    # display warning and list of available jvm
    print_usage()
    print('\nWARNING: [ cells / %s / nodes / %s / servers / %s ] not available!' % (cell, node, serv))
    print_jvms()
  
# =======================================================================================================================
# for WAS 6: __name__ == "main"
if __name__ == "__main__" or __name__ == "main":
  jvm_generate_dump( *sys.argv)
  # sys.exit()
else:
  try:
    # import AdminConfig, AdminControl, AdminApp, AdminTask, Help
    import lineSeparator
  except:
    pass

