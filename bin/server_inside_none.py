# ===========================================
# generate JVM dumps, heap, system, threads
# for one or more servers
# ===========================================
script_name = "server_inside_none.py"

# ================================================
# show server inside hierarchy
#   need to show transportChannels
#   ObjectType: [ attribute1, attribute2, attribute3.sub_attribute, attribute2:ObjectType]
# ================================================
type_attributes = { 
  'ActivitySessionService':     ['defaultTimeout', 'enable'],
  'ApplicationProfileService':  ['enable'],
  'ApplicationServer':          ['applicationClassLoadingMode', 'applicationClassLoaderPolicy'],
  'ConnectionPool':             ['agedTimeout', 'connectionTimeout', 'minConnection', 'maxConnection', 'unusedTimeout'],
  'DynamicCache':               ['cacheSize', 'enable', 'replicationType'],
  'EJBContainer':               ['inactivePoolCleanupInterval', 'asyncSettings.futureTimeout', 'asyncSettings.maxThreads', 'cacheSettings.cacheSize', 'cacheSettings.cleanupInterval'],
  'TransactionService':         ['asyncResponseTimeout', 'clientInactivityTimeout', 'enable'],
  'WebContainer':               ['asyncIncludeTimeout', 'defaultAsyncServletTimeout', 'sessionAffinityTimeout','properties:Properties'],
  'SessionManager':             ['accessSessionOnTimeout', 'defaultCookieSettings.name', 'defaultCookieSettings.maximumAge', 'enable', 'maxWaitTime', 'tuningParams.invalidationTimeout', 'tuningParams.maxInMemorySessionCount'],
  'CellManager':                ['CELL_DISCOVERY_ADDRESS:EndPoint', 'name'],
  # 'CellManager':                ['CELL_DISCOVERY_ADDRESS.host', 'CELL_DISCOVERY_ADDRESS.port', 'name'],
  'CompensationService':        ['enable'],
  'DataSource':                 ['name', 'authDataAlias', 'statementCacheSize', 'connectionPool:ConnectionPool', 'propertySet:resourceProperties'],
  'resourceProperties':         ['resourceProperties:resourceProperty'],
  'resourceProperty':           ['name', 'value'],
  'EventInfrastructureService': ['enable'],
  'HAManagerService':           ['activateEnabled', 'coreGroupName', 'enable', 'isAlivePeriodSec', 'threadPool:ThreadPool'],
  'HighPerformanceExtensibleLogging': ['enable', 'startupTraceSpec'],
  'I18NService':                ['enable'],
  'JAASAuthData':               ['alias', 'userId'],
  'JDBCProvider':               ['name', 'xa', 'classpath'],
  'JobManager':                 ['databaseMaxReturn', 'defaultJobExpiration', 'threadPool:ThreadPool'],
  'NameServer':                 ['BOOTSTRAP_ADDRESS:EndPoint'], 
  # 'NameServer':                 ['BOOTSTRAP_ADDRESS.host', 'BOOTSTRAP_ADDRESS.port'], 
  'ObjectPoolService':          ['enable'],
  'PluginConfigService':        ['enable'],
  'SchedulerService':           ['enable'],
  'Server':                     ['adjustPort', 'developmentMode', 'errorStreamRedirect.fileName', 'errorStreamRedirect.maxNumberOfBackupFiles', 'name', 'outputStreamRedirect.fileName', 'outputStreamRedirect.maxNumberOfBackupFiles', 'parallelStartEnabled', 'serverType'],
  'AdminService':               ['enable'],
  'CoreGroupBridgeService':     ['enable'],
  'DiagnosticProviderService':  ['enable', 'startupStateCollectionSpec'],
  'HTTPAccessLoggingService':   ['accessLog.filePath', 'accessLogFormat', 'enable', 'errorLog.filePath', 'errorLogLevel'],
  'ObjectRequestBroker':        ['CSIV2_SSL_MUTUALAUTH_LISTENER_ADDRESS:EndPoint', 'CSIV2_SSL_SERVERAUTH_LISTENER_ADDRESS:EndPoint', 'ORB_LISTENER_ADDRESS:EndPoint', 'SAS_SSL_SERVERAUTH_LISTENER_ADDRESS:EndPoint', 'connectionCacheMaximum', 'connectionCacheMinimum', 'enable', 'locateRequestTimeout', 'requestRetriesCount', 'requestRetriesDelay', 'requestTimeout', 'threadPool:ThreadPool'],
  # 'ObjectRequestBroker':        ['CSIV2_SSL_MUTUALAUTH_LISTENER_ADDRESS.host', 'CSIV2_SSL_MUTUALAUTH_LISTENER_ADDRESS.port', 'CSIV2_SSL_SERVERAUTH_LISTENER_ADDRESS.host', 'CSIV2_SSL_SERVERAUTH_LISTENER_ADDRESS.port', 'ORB_LISTENER_ADDRESS.host', 'ORB_LISTENER_ADDRESS.port', 'SAS_SSL_SERVERAUTH_LISTENER_ADDRESS.host', 'SAS_SSL_SERVERAUTH_LISTENER_ADDRESS.port', 'connectionCacheMaximum', 'connectionCacheMinimum', 'enable', 'locateRequestTimeout', 'requestRetriesCount', 'requestRetriesDelay', 'requestTimeout', 'threadPool:ThreadPool'],
  'PMIService':                 ['enable', 'statisticSet'],
  'RASLoggingService':          ['enable', 'enableCorrelationId', 'serviceLog.enabled', 'serviceLog.name'],
  'SIBService':                 ['enable'],
  'ThreadPoolManager':          ['enable', 'threadPools:ThreadPool'],
  'TPVService':                 ['enable'],
  'TraceService':               ['enable', 'startupTraceSpecification', 'traceLog.fileName', 'traceLog.maxNumberOfBackupFiles', 'traceLog.rolloverSize'],
  'TransportChannelService':    ['chains:Chain', 'enable', 'transportChannels:Channel'],
  'StartupBeansService':        ['enable'],
  'WorkAreaPartitionService':   ['enable'],
  'WorkAreaService':            ['enable', 'enableWebServicePropagation', 'maxReceiveSize', 'maxSendSize'],
  'WorkManagerService':         ['enable'],
  'WorkloadManagementServer':   ['name'],
  'ThreadPool':                 ['name', 'inactivityTimeout', 'isGrowable', 'maximumSize', 'minimumSize'],
  'Channel':                    ['name', 'endPointName', 'inactivityTimeout', 'persistentTimeout', 'keepAlive', 'enableLogging', 'maxOpenConnections', 'threadPool.name'],
  'Chain':                      ['name', 'enable', 'transportChannels:Channel'],
  'MessageListenerService':     ['enable', 'threadPool:ThreadPool'],
  'EndPoint':                   ['host', 'port'],
  'Properties':                 ['name','value','description']
  }


  # 'Channel':                    ['name'],
  # 'HAManagerService':           ['activateEnabled', 'coreGroupName', 'enable', 'isAlivePeriodSec', 'threadPool.inactivityTimeout', 'threadPool.isGrowable', 'threadPool.maximumSize', 'threadPool.minimumSize', 'threadPool.name'],

def show_parameters3( id, id_type, level, parent_param=""):
  # s: [ type, id, parent_id]
  if not id_type in type_attributes.keys():
    try:
      p_value = AdminConfig.showAttribute( id, 'name')
      print "    "*(level+1) +  "%s %s" % ('name', p_value)
    except:
      print "%s : no attributes defined and 'name' attribute is not available. Please define some attributes for this object type." % id_type
    return
  else: 
    for p in type_attributes[ id_type]:
      if p.find(':') >= 0: 
        # p = [param:type of value] when value contains a list of id
        params = p.split(':')
        # print "    "*(level+1) +  "%s" % p
        print
        for p_id in AdminConfig.showAttribute( id, params[0]).replace('[','').replace(']','').split( " "):
          if p_id: 
            print "    "*(level+1) +  "%s" % params[0],
            show_parameters3( p_id, params[1], level+1, params[0])
          print
      elif p.find('.') >= 0:
        # p = [param.param(for id in value)] when value contains an id
        params = p.split( '.')
        try:
          p_value = AdminConfig.showAttribute( AdminConfig.showAttribute( id, params[0]), params[1])
          if parent_param:
            print "    "*(level+1) +  "%s %s" % (p, p_value),
          else:
            print "    "*(level+1) +  "%s %s" % (p, p_value)
        except:
          pass
      else:
        # p = param when value contains a simple value
        try:
          p_value = AdminConfig.showAttribute( id, p)
          if parent_param:
            print "%-30s" % (p +":"+ p_value), 
          else:
            print "    "*(level+1) +  "%s %s" % (p, p_value)
        except:
          pass
    return    

# def show_parameters2( s, level):
#  # for p in AdminConfig.show( s[1]).split( lineSeparator):
#  #  print "    "*(level+1) +  "%s" % p
#  for p in type_attributes[ s[0]]:
#    if p.find(':') >= 0:
#      # if p = x:y: x=attribute containing a list of id of type y
#      params = p.split(':')
#      for p in AdminConfig.showAttribute( s[1], params[0]).replace('[','').replace(']','').split( " "):
#        ptype = AdminConfig.getObjectType( p)
#        # print "%s : %s" % ( ptype, p)
#        print "    "*(level+1) +  "%-20s" % params[0],
#        for pp in type_attributes[ ptype]:
#          # print "%s : %s" % ( ptype, p)
#          param = AdminConfig.showAttribute( p, pp)
#          # print "    "*(level+1) +  "%s.%s %s" % (pname, pp, param)
#          print " %-30s" % (pp + ":" + param),
#        print
#    else:
#      # if p = x.y: x=attribute containing en id, y=param to retrieve using x id
#      params = p.split( '.')
#      if len(params) == 1:
#        param = AdminConfig.showAttribute( s[1], params[0])
#        print "    "*(level+1) +  "%s %s" % (p, param)
#      if len(params) == 2:
#        param = AdminConfig.showAttribute( AdminConfig.showAttribute( s[1], params[0]), params[1])
#        print "    "*(level+1) +  "%s %s" % (p, param)
#  print
#  return

# def show_parameters( s, level):
#  # for p in AdminConfig.show( s[1]).split( lineSeparator):
#  for p in type_attributes[ s[0]]:
#    params = p.split( '.')
#    if len(params) == 1:
#      param = AdminConfig.showAttribute( s[1], params[0])
#      print "    "*(level+1) +  "%s %s" % (p, param)
#    if len(params) == 2:
#      param = AdminConfig.showAttribute( AdminConfig.showAttribute( s[1], params[0]), params[1])
#      print "    "*(level+1) +  "%s %s" % (p, param)
#  print
#  return

def show_children( level, parent, hierarchy, detail):
  for element in hierarchy:
    # show current element if parents are parent and descendante children
    # s: 0:objectType 1:id 2:parent id
    s = element.split(";")
    if s[2] == parent:
      # print "    "*level +  "%s" % s[0]
      # if detail > 0: print "    "*(level+1) +  "%s" % s[1] 
      if detail == 0: print        "    "*level +  "%s" % s[0]
      if detail > 0 : print "\n" + "    "*level +  "%s   %s" % ( s[0], s[1])
      if detail > 1 :
        show_parameters3( s[1], s[0], level)
      show_children( level+1, s[1], hierarchy, detail)
  return

def show_objects_hierarchy( id, liste, detail):
  hierarchy = []
  hierarchy.append("%s;%s;%s" % (AdminConfig.getObjectType( id), id, ""))
  # construct the hierarchy : list of "type;id;parent_id" definitions
  for element in liste:
    try:
      i = AdminConfig.list( element, id)
    except:
      i = 0
    if i:
      for j in i.split( lineSeparator):
        # print "Adding %s in hierarchy" % j
        # get parent: for service get service.context, for component get component.parentComponent
        parent = None
        try:
          parent = AdminConfig.showAttribute( j, "context")
        except:
          try:
            parent = AdminConfig.showAttribute( j, "parentComponent")
          except:
            pass
        if parent == None: parent = ""
        c = "%s;%s;%s" % (AdminConfig.getObjectType( j), j, parent)
        if c not in hierarchy: hierarchy.append( c)
  hierarchy.sort()
  # display the hierarchy
  for element in hierarchy:
    # print element
    level = 1
    parent = ""
    # show current element if parents are parent and descendante children
    # s: 0:objectType 1:id 2:parent id
    s = element.split(";")
    if s[2] == parent:
      # print "    "*level +  "%s" % s[0]
      # if detail > 0: print "    "*(level+1) +  "%s" % s[1] 
      if detail == 0: print        "    "*level +  "%s" % s[0]
      if detail > 0 : print "\n" + "    "*level +  "%s   %s" % ( s[0], s[1])
      if detail > 1 : 
        show_parameters3( s[1], s[0], level)
      show_children( level+1, s[1], hierarchy, detail)
  return

def show_server_hierarchy( cell, node, server, detail):
  detail = int( detail)
  components = "JAASAuthData, DataSource, JDBCProvider, SecurityServer, NodeAgent, EJBContainer, JobManager, JMSServer, SecurityServer, Agent, ServerComponent, WebContainer, ForeignServer, PortletContainer, SystemMessageServer, ExternallyManagedHTTPServer, WorkloadManagementServer, ExternalFileService, ApplicationServer, ApplicationContainer, WebServer, NameServer, SIPContainer, CellManager, Proxy, OnDemandRouter, ProxyServer"
  services = "DiagnosticProviderService, FileTransferService, ConfigSynchronizationService, VisualizationDataService, SchedulerService, EventInfrastructureService, I18NService, CustomService, SessionManager, RASLoggingService, HighPerformanceExtensibleLogging, JavaPersistenceAPIService, CompensationService, AdminService, PluginConfigService, CoreGroupBridgeService, StartupBeansService, CacheInstanceService, WorkAreaService, WorkAreaPartitionService, SIBService, TraceService, TPVService, ApplicationManagementService, ApplicationProfileService, WorkManagerService, DebugService, TransportChannelService, WSByteBufferService, TransactionService, DynamicCache, ObjectRequestBroker, AppPlacementController, MessageListenerService, HealthController, PMIService, ThreadPoolManager, ActivitySessionService, HAManagerService, ObjectPoolService, HTTPAccessLoggingService"
  _components = []
  _services = []
  [_components.append( x) for x in components.replace(" ","").split(",") if x not in _components]
  [_services.append( x) for x in services.replace(" ","").split(",") if x not in _services]
  _services_components = _services + _components
  _components.sort()
  _services.sort()
  _services_components.sort()
  # print _services_components
  # ----------------------------------------------------------
  srvs = AdminConfig.list("ServerEntry").split( lineSeparator)
  # print srvs
  found = 0
  found_ports = {}
  for srv in srvs:
    print
    cell_node_server = srv.split('|')[0].split('/')
    _cell = cell_node_server[1]
    _node = cell_node_server[3]
    _serv = AdminConfig.showAttribute( srv, "serverName")
    server_type = AdminConfig.showAttribute( srv, 'serverType')
    if not found and (cell == 'all') and (node == 'all') and (serv == 'all'):
      found = 1
      print('-'*20)
      print "[ cells / %s ]" % _cell
      # id = AdminConfig.getid( '/Server:%s/' % server)
      id = AdminConfig.getid( '/Cell:%s/' % _cell)
      if id:
        print "-"*20            
        # services
        show_objects_hierarchy( id, _services_components, detail)
      # return
    if (_cell == cell or cell == 'all') and (_node == node or node == 'all') and (_serv == serv or serv == 'all'):
      found = 1
      print('-'*20)
      print "[ cells / %s / nodes / %s / servers / %s ] of type %s" % ( _cell, _node, _serv, server_type)
      # id = AdminConfig.getid( '/Server:%s/' % server)
      id = AdminConfig.getid( '/Cell:%s/Node:%s/Server:%s/' % ( _cell, _node, _serv))
      if id:
        print "-"*20            
        # services
        show_objects_hierarchy( id, _services_components, detail)
  if not found:
    print "Server not found..."
    print_jvms() 
  return

def print_usage():
  print('\nUsage: wsadmin.sh [-conntype none] -lang jython -f <%s> <cell|all> <node|all> <server|all> <details_level>     where details_level = [0|1|2]' % script_name)
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


# =======================================================================================================================
# for WAS 6: __name__ == "main"
if __name__ == "__main__" or __name__ == "main":
  # test parameter
  print('-'*20)
  if len( sys.argv) >= 4:
    cell = sys.argv[0]
    node = sys.argv[1]
    serv = sys.argv[2]
    if len( sys.argv) > 3: details_level = int( sys.argv[3])
    else: details_level = 0
    show_server_hierarchy( *sys.argv)
    # show_server_hierarchy( 'dmgr', 0)
  else:
    print_usage()
    print_jvms()
  # sys.exit()
else:
  try:
    # import AdminConfig, AdminControl, AdminApp, AdminTask, Help
    import lineSeparator
  except:
    pass

