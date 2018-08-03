#!/usr/bin/env python

import numpy as np
import subprocess
import jpype

# get class path
classpath = subprocess.check_output(['hadoop','classpath'])
classpath = '.:'+classpath
print(classpath)



# jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=%s" % classpath)

# get the Java classes we want to use
# DefaultExtractor = jpype.JPackage("de").l3s.boilerpipe.extractors.DefaultExtractor

# call them !
# print DefaultExtractor.INSTANCE.getText(jpype.java.net.URL("http://blog.notmyidea.org"))