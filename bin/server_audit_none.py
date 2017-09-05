# ===========================================
# list information on servers
# for one or more servers
# and check for duplicated ports
# ===========================================
script_name = "server_audit_none.py"

import re, sys

def print_usage():
  print('\nUsage: wsadmin.sh -conntype none -lang jython -f <%s> <cell|all> <node|all> <server|all> [details]' % script_name)
  print

def print_servers():
  """
    print list of available Servers
  """
  print('\nDefined Servers are:')
  jvms = AdminConfig.list('ServerEntry').split( lineSeparator)
  for jvm in jvms:
    cell_node_server = jvm.split('|')[0].split('/')
    _cell = cell_node_server[1]
    _node = cell_node_server[3]
    _serv = AdminConfig.showAttribute( jvm, "serverName")
    print('  [ cells / %s / nodes / %s / servers / %s ]' % (_cell, _node, _serv))
  print
  return

def server_audit( *argv):
  # test parameter
  print('-'*20)
  if len( sys.argv) >= 3: 
    cell = sys.argv[0]
    node = sys.argv[1]
    serv = sys.argv[2]
    print('Listing servers for server [ cells / %s / nodes / %s / servers / %s ]' % (cell, node, serv))
    if len( sys.argv) > 3: 
      details = 1
    else:
      details = 0
  else:
    print_usage()
    print_servers()
    return
    # sys.exit()
  
  # get all servers
  # srvs = AdminConfig.list("ServerEntry", '(cells/%s/nodes/%s|serverindex.xml)' % (cell, node)).split( lineSeparator)
  srvs = AdminConfig.list("ServerEntry").split( lineSeparator)
  # print srvs
  found = 0
  found_ports = {}
  for srv in srvs:
    cell_node_server = srv.split('|')[0].split('/')
    _cell = cell_node_server[1]
    _node = cell_node_server[3]
    _serv = AdminConfig.showAttribute( srv, "serverName")
    server_type = AdminConfig.showAttribute( srv, 'serverType')
    if (_cell == cell or cell == 'all') and (_node == node or node == 'all') and (_serv == serv or serv == 'all'):
      found = 1
      if details: print('-'*20)
      print "[ cells / %s / nodes / %s / servers / %s ] of type %s" % (_cell, _node, _serv, server_type)
      if not details: continue
      # ---------------------
      # Showing directories properties
      # ---------------------
      print
      print "  Directories:"
      for var in AdminConfig.list('VariableSubstitutionEntry', "*%s*" % _node).split( lineSeparator):
        var_name = AdminConfig.showAttribute( var, 'symbolicName')
        var_value = AdminConfig.showAttribute( var, 'value')
        # print "VAR %s: %s" % ( var_name, var_value)
        if var_name in ['WAS_INSTALL_ROOT', 'USER_INSTALL_ROOT', 'LOG_ROOT']:
          print("  %40s:%22s %s" % (var_name, '', var_value))

      # ---------------------
      # Listing ports in used
      # ---------------------
      print
      print "  Ports:"
      ports = {}
      neps = AdminConfig.list("NamedEndPoint", srv).split( lineSeparator)
      # print neps
      # print len( neps)
      for nep in neps:
        epname = AdminConfig.showAttribute( nep, "endPointName")
        ep = AdminConfig.showAttribute( nep, "endPoint")
        host = AdminConfig.showAttribute( ep, "host")
        port = AdminConfig.showAttribute( ep, "port")
        if port not in ports.keys():
          ports[ port] = []
        ports[ port].append( { 'host':host, 'epname':epname})
        if port not in found_ports.keys():
          found_ports[ port] = []
        found_ports[ port].append( '%40s:%20s:%6s [ cells / %s / nodes / %s / servers / %s ]' % (epname, host, port, _cell, _node, _serv)) 
      # sort result and print
      ports_list = ports.keys()
      ports_list.sort()
      for port in ports_list:
        for p in ports[ port]:
          print('  %40s:%20s:%6s' % ( p['epname'], p['host'], port))
      # ---------------------
      # Showing Server deployed applications
      # ---------------------
      print
      print "  Deployed applications:"
      for app in AdminConfig.showAttribute( srv, 'deployedApplications').split(';'):
        print("    %s" % app)
      # ---------------------
      # Showing Server properties
      # ---------------------
      print
      print "  Properties:"
      for prop in AdminConfig.list( 'Property', '(cells/%s/nodes/%s/servers/%s|server.xml)' % (_cell, _node, _serv)).split( lineSeparator):
        if prop != '':
          # if AdminConfig.showAttribute( prop, 'name').find( 'IBM') == 0: 
          print("    %-30s %s" % (AdminConfig.showAttribute( prop, 'name'), AdminConfig.showAttribute( prop, 'value')))
      # ---------------------
      # Showing JVM properties
      # ---------------------
      print
      print "  JVM:"
      jvm = AdminConfig.list( 'JavaVirtualMachine', '(cells/%s/nodes/%s/servers/%s|server.xml)' % (_cell, _node, _serv))
      for jvm_arg in AdminConfig.show( jvm).split( lineSeparator):
        print("    %s" % jvm_arg)

      print
      print "  JVM systemProperties:"
      for jvm_arg in AdminConfig.list( 'Property', jvm).split( lineSeparator):
        if jvm_arg:
          print("    [%s %s]" % (AdminConfig.showAttribute( jvm_arg, 'name'), AdminConfig.showAttribute( jvm_arg, 'value')))
      # ---------------------
      # Showing WebContainer properties
      # ---------------------
      print
      print "  WebContainer:"
      webcontainer =  AdminConfig.list( 'WebContainer', '(cells/%s/nodes/%s/servers/%s|server.xml)' % (_cell, _node, _serv))
      if webcontainer:
        for web_arg in AdminConfig.show( webcontainer).split( lineSeparator):
          print("    %s" % web_arg)

        print
        print "  WebContainer properties:"
        for web_arg in AdminConfig.list( 'Property', webcontainer).split( lineSeparator):
          if web_arg:
            print("    [%s %s]" % (AdminConfig.showAttribute( web_arg, 'name'), AdminConfig.showAttribute( web_arg, 'value')))
      
      # ---------------------
      # Showing ThreadPools properties
      # ---------------------
      print
      print "  ThreadPool:"
      threadpools =  AdminConfig.list( 'ThreadPool', '(cells/%s/nodes/%s/servers/%s|server.xml)' % (_cell, _node, _serv)).split( lineSeparator)
      if threadpools:
        for thread in threadpools:
          try:
            inactivityTimeout = AdminConfig.showAttribute( thread, 'inactivityTimeout')
            isGrowable = AdminConfig.showAttribute( thread, 'isGrowable')
            maximumSize = AdminConfig.showAttribute( thread, 'maximumSize')
            minimumSize = AdminConfig.showAttribute( thread, 'minimumSize')
            name = AdminConfig.showAttribute( thread, 'name')
            print "    %40s  minimumSize:%5s  maximumSize:%5s  isGrowable:%6s  inactivityTimeout:%6s" % ( name, minimumSize, maximumSize, isGrowable, inactivityTimeout)
          except:
            pass
        print
      
      # ---------------------
      # Showing JAAS alias
      # ---------------------
      print
      print "  JAASauthAlias:"
      jaasauths = AdminConfig.list('JAASAuthData').split( lineSeparator)
      jaas_auth = {}
      for jaasauth in jaasauths:
        if jaasauth != '':
          try:
            ja_alias = AdminConfig.showAttribute( jaasauth, 'alias')
            ja_userid = AdminConfig.showAttribute( jaasauth, 'userId')
            jaas_auth[ ja_alias] = ja_userid
            print "    %40s  userId:  %s" % ( ja_alias, ja_userid)
          except:
            pass

      # ---------------------
      # Showing DataSources properties
      # ---------------------
      print
      print "  DataSource:"
      for ds in AdminConfig.list( 'DataSource').split( lineSeparator):
        ds_name = AdminConfig.showAttribute( ds, 'name')
        ds_auth = AdminConfig.showAttribute( ds, 'authDataAlias')
        if ds_auth in jaas_auth.keys(): ds_auth_jaas = jaas_auth[ ds_auth]
        else: ds_auth_jaas = "?"
        ds_cach = AdminConfig.showAttribute( ds, 'statementCacheSize')
        print "    %40s  statemenCacheSize:%6s  authDataAlias:%s (%s)" % ( ds_name, ds_cach, ds_auth, ds_auth_jaas)
        # connectionPool infos (agedTimeout, connectionTimeout, maxConnections, minConnections, unusedTimeout)
        ds_pool = AdminConfig.showAttribute( ds, 'connectionPool')
        ds_pool_agedtm = AdminConfig.showAttribute( ds_pool, 'agedTimeout')
        ds_pool_conntm = AdminConfig.showAttribute( ds_pool, 'connectionTimeout')
        ds_pool_mincon = AdminConfig.showAttribute( ds_pool, 'minConnections')
        ds_pool_maxcon = AdminConfig.showAttribute( ds_pool, 'maxConnections')
        ds_pool_unustm = AdminConfig.showAttribute( ds_pool, 'unusedTimeout')
        print "    %40s     minConnections:%6s  maxConnections:%6s  agedTimeout:%6s  connectionTimeout:%6s  unusedTimeout:%6s" % ( '', ds_pool_mincon, ds_pool_maxcon, ds_pool_agedtm, ds_pool_conntm, ds_pool_unustm)
        # propertySet infos (URL)
        ds_prop = AdminConfig.showAttribute( ds, 'propertySet')
        ds_prop_resour = AdminConfig.showAttribute( ds_prop, 'resourceProperties') 
        ds_prop_reslst = re.compile(  '(\(cells/.*?\))').findall( ds_prop_resour)
        for res in ds_prop_reslst:
          ds_prop_name = AdminConfig.showAttribute( res, 'name')
          if ds_prop_name.lower().find('url') == 0:
            ds_prop_value = AdminConfig.showAttribute( res, 'value')
            print "    %40s  url:%s" % ( '', ds_prop_value)
        print

      # ---------------------
      # Showing PMI properties
      # ---------------------
      print
      print "  PMI:"
      pmi =  AdminConfig.list( 'PMIService', '(cells/%s/nodes/%s/servers/%s|server.xml)' % (_cell, _node, _serv))
      if pmi != '':
        for pmi_arg in AdminConfig.show( pmi).split( lineSeparator):
          print("    %s" % pmi_arg)
      print

  # sort and print duplicated ports
  dups = [x for x in found_ports.keys() if len( found_ports[x]) > 1]
  found_duplicate = len( dups)
  if found_duplicate:
    print('-'*20)
    print "Number of duplicated ports: %d" % found_duplicate
    ports_list = found_ports.keys()
    ports_list.sort()
    for port in ports_list:
      if len( found_ports[ port]) > 1:
        print
        for ep in found_ports[ port]:
          print ep
  
  # if found nothing, list available server entries
  if not found:
    # display warning and list of available server entries
    print('\nWARNING: [ cells / %s / nodes / %s / servers / %s ] not found!' % (cell, node, serv))
    print_usage()
    print_servers()
  
# =======================================================================================================================
# for WAS 6: __name__ == "main"
if __name__ == "__main__" or __name__ == "main":
  server_audit( *sys.argv)
  # sys.exit()
else:
  try:
    # import AdminConfig, AdminControl, AdminApp, AdminTask, Help
    import lineSeparator
  except:
    pass

