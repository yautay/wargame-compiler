from support import *
if __name__=='__main__':
    result=command(sys.argv[1],sys.argv[2:])
    sys.exit(result['exit_code'])
