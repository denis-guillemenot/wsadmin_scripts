# ===========================================
# show/set JVM genericJvmArguments
# for one or more servers
# ===========================================
script_name = "jvm_generic_arguments_none.py"

import sys

def print_usage():
  print('\nUsage: wsadmin.sh -conntype none -lang jython -f <%s> <cell|all> <node|all> <server|all> ["<jvm arguments>"]' % script_name)
  print

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

def jvm_generic_arguments( *argv):
  # test parameter
  print('-'*20)
  if len( argv) >= 3: 
    cell = argv[0]
    node = argv[1]
    serv = argv[2]
    if len( argv) == 4:
      mode = argv[3]
      print('Setting JVM genericJvmArguments for [ cells / %s / nodes / %s / servers / %s ] to %s' % (cell, node, serv, mode))
    else:
      mode = 'disp'
      # print_usage()
      print('Showing JVM genericJvmArguments for [ cells / %s / nodes / %s / servers / %s ]' % (cell, node, serv))
  else:
    print_usage()
    print_jvms()
    return
    # sys.exit()
  
  # setting JVM genericJvmArguments for selected jvm
  found = 0
  only_application_server = 'true'
  jvms = AdminConfig.list('JavaVirtualMachine').split( lineSeparator)
  for jvm in jvms:
    cell_node_server = jvm.split('|')[0].split('/')
    _cell = cell_node_server[1]
    _node = cell_node_server[3]
    _serv = cell_node_server[5]
    # _serv = AdminConfig.showAttribute( jvm, "serverName")
    # retrieve server type
    server_type = AdminConfig.showAttribute( AdminConfig.list( 'Server', jvm), 'serverType')
    # if 'all' is used then activate only if server type is APPLICATION_SERVER
    # else if 'all' is not used then user knows what he does so activate even if server type is not APPLICATION_SERVER
    if (cell != 'all') and (node != 'all') and (serv != 'all'):
      only_application_server = 'false'
    # do if only current jvm is targeted
    if (_cell == cell or cell == 'all') and (_node == node or node == 'all') and (_serv == serv or serv == 'all'):
      found = found + 1
      # print('-'*20)
      current_gen = AdminConfig.showAttribute( jvm, 'genericJvmArguments')
      if mode != 'disp':
        if (server_type == 'APPLICATION_SERVER') or (only_application_server == 'false'):
          AdminConfig.modify( jvm, "[[genericJvmArguments '%s']]" % mode)
          AdminConfig.save()
          # print AdminConfig.show( jvm)
          new_gen = AdminConfig.showAttribute( jvm, 'genericJvmArguments')
          modified = 1
        else:
          modified = 0
      # print results
      print
      print '[ cells / %s / nodes / %s / servers / %s ]' % ( _cell, _node, _serv)
      print '  [servetype %s]' % server_type
      if mode != 'disp':
        if modified:
          print '  [genericJvmArguments %s => %s]' % ( current_gen, new_gen)
        else:
          print '  [genericJvmArguments %s]' % current_gen
          print "  No modification... To modify this jvm (%s), do not use 'all' in the parameters list" % server_type
      else:
        print '  [genericJvmArguments %s]' % current_gen
  
  # display list of jvm available if no match
  if not found:
    # display warning and list of available jvm
    print_usage()
    print('\nWARNING: [ cells / %s / nodes / %s / servers / %s ] not found!' % (cell, node, serv))
    print_jvms()
  
# =======================================================================================================================
# for WAS 6: __name__ == "main"
if __name__ == "__main__" or __name__ == "main":
  jvm_generic_arguments( *sys.argv)
  # sys.exit()
else:
  try:
    # import AdminConfig, AdminControl, AdminApp, AdminTask, Help
    import lineSeparator
  except:
    pass

