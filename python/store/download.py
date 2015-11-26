import os
import logging

def on_complete(filepath, filepath_ready):
    logging.debug("on_complete filepath=" + filepath + " filepath_ready="+filepath_ready)
    if os.path.isfile(filepath_ready):
        if os.path.islink(filepath_ready):
            linkpath = os.readlink( filepath_ready )
            if linkpath == filepath:
                logging.debug("symlink from:"+filepath+" to:"+filepath_ready+ " already exists")
                return 1
        os.remove(filepath_ready)
    logging.info("symlinking completed file to ready dir -> from:"+filepath+" to:"+filepath_ready)
    os.symlink(filepath,filepath_ready)
    #shutil.move(filepath,filepath_ready)


logger = logging.getLogger('store.download')