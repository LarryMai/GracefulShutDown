import sys, os, logging,  traceback
import json
import shutil
from subprocess import Popen, PIPE
import subprocess
import time

logger = logging.getLogger(__name__)

INSTALLATION_ROOT_DIR = "/opt" 
APP_NAME="graceful_shutdown"
BUILD_ARCH="{BUILD_ARCH}"
TAR_GZ_FILE= "{}.{}.tar.gz".format(APP_NAME, BUILD_ARCH)
RUN_SH_FILE="run.sh"       
SERVICE_FILE="{}.service".format(APP_NAME)  

INSTALL_DIR=os.path.join(INSTALLATION_ROOT_DIR, APP_NAME)
INSTALL_BIN_DIR=os.path.join(INSTALL_DIR, BUILD_ARCH)


def extract_file(tar_gz_file_path: str, target_folder: str, slient: bool=True):

    success =False
    msg = ''
    options = "-zxvf"
    if slient:
        options = "-zxf"
    cmd = "tar {} {} -C {}".format(options, tar_gz_file_path ,target_folder)
    logger.debug(cmd)
    
    try:
        process = subprocess.Popen(cmd.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output,error = process.communicate()
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.info(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        return success, 'internal error'
    
    # logger.debug('output : {}'.format(output)) 
    if process.returncode != 0:
        logger.debug('error : {}'.format(error.decode('utf-8')))  
        msg =error.decode('utf-8')
    else:
        success = True
    
    return success,  msg

def enable_service(service_name):
    
    success =False
    msg = ''
    cmd = "systemctl enable {}".format(service_name)
    logger.debug(cmd)
    
    try:
        process = subprocess.Popen(cmd.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output,error = process.communicate()
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.info(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        return success, 'internal error'
    
    # logger.debug('output : {}'.format(output)) 
    if process.returncode != 0:
        logger.debug('error : {}'.format(error.decode('utf-8')))  
        msg =error.decode('utf-8')
    else:
        success = True
    
    return success,  msg

def disable_service(service_name):
    success =False
    msg = ''
    cmd = "systemctl disable {}".format(service_name)
    logger.debug(cmd)
    
    try:
        process = subprocess.Popen(cmd.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output,error = process.communicate()
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.info(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        return success, 'internal error'
    
    # logger.debug('output : {}'.format(output)) 
    if process.returncode != 0:
        logger.debug('error : {}'.format(error.decode('utf-8')))  
        msg =error.decode('utf-8')
    else:
        success = True
    
    return success,  msg

def daemon_reload():
    success =False
    msg = ''
    cmd = "systemctl daemon-reload"
    logger.debug(cmd)
    
    try:
        process = subprocess.Popen(cmd.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output,error = process.communicate()
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.info(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        return success, 'internal error'
    
    # logger.debug('output : {}'.format(output)) 
    if process.returncode != 0:
        logger.debug('error : {}'.format(error.decode('utf-8')))  
        msg =error.decode('utf-8')
    else:
        success = True
    
    return success,  msg    

def start_service(service_name):
    success =False
    msg = ''
    cmd = "systemctl start {}".format(service_name)
    logger.debug(cmd)
    
    try:
        process = subprocess.Popen(cmd.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output,error = process.communicate()
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.info(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        return success, 'internal error'
    
    # logger.debug('output : {}'.format(output)) 
    if process.returncode != 0:
        logger.debug('error : {}'.format(error.decode('utf-8')))  
        msg =error.decode('utf-8')
    else:
        success = True
    
    return success,  msg

def stop_service(service_name):
    success =False
    msg = ''
    cmd = "systemctl stop {}".format(service_name)
    logger.debug(cmd)
    
    try:
        process = subprocess.Popen(cmd.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output,error = process.communicate()
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.info(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        return success, 'internal error'
    
    # logger.debug('output : {}'.format(output)) 
    if process.returncode != 0:
        logger.debug('error : {}'.format(error.decode('utf-8')))  
        msg =error.decode('utf-8')
    else:
        success = True
    
    return success,  msg

if __name__ == '__main__':

    # here, assume the executor has admin previliage    
    logFileName=os.path.join(INSTALL_DIR, "install.log")
    os.makedirs(os.path.dirname(logFileName), exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(filename)s(%(lineno)d) %(message)s'
    )
    force_start=True
    current_dir = os.path.abspath(os.path.dirname(__file__))
    logger.info("current_dir: " + current_dir)
    
    # check ota file exists
    ota_file = os.path.join(current_dir, TAR_GZ_FILE)
    if not os.path.exists(ota_file):
        logger.info("{} doesn't exist", ota_file)
        os._exit(-1)
    
    # shutdown service
    if os.path.exists(os.path.join("/etc/systemd/system", SERVICE_FILE)):
        stop_service(SERVICE_FILE)
        disable_service(SERVICE_FILE)
        logger.info("shutdown service {} completed.".format(SERVICE_FILE))
    
    if not os.path.exists(INSTALL_DIR):
        os.makedirs(INSTALL_DIR, exist_ok=True)
    

            
    # extract tar.gz to INSTALL_BIN_DIR folder
    success, error=extract_file(ota_file, INSTALL_DIR)
    if not success:
        logger.info("extract file({}) with error: {}", ota_file, error)
        os._exit(-2)
        
    logger.info("begin to copy run.sh")
    source_run_sh_file = os.path.join(current_dir, RUN_SH_FILE)
    dest_run_sh_file = os.path.join(INSTALL_DIR, RUN_SH_FILE)
    shutil.copyfile(source_run_sh_file, dest_run_sh_file)
    os.chmod(dest_run_sh_file, 0o755)
    logger.info("copy run.sh completed")

    logger.info("install service")
    source_service_file = os.path.join(current_dir, SERVICE_FILE)
    dest_service_file = os.path.join("/etc/systemd/system/", SERVICE_FILE)
    shutil.copy(source_service_file, dest_service_file)
    success, error = daemon_reload()
    if not success:
        logger.info("daemon_reload failed")
        os._exit(-1)
    success, error = enable_service(SERVICE_FILE)
    if not success:
        logger.info("enable {} failed".format(SERVICE_FILE))
        os._exit(-1)
    
    logger.info("install service completed")
    
    if force_start:
        success, error = start_service(SERVICE_FILE)
        if not success:
            logger.info("start {} failed".format(SERVICE_FILE))
            os._exit(1)
            
    logging.info("completed")