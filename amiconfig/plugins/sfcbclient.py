#
# Copyright (c) SAS Institute Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import base64
import os

from conary.lib import util
from amiconfig.plugin import AMIPlugin

class AMIConfigPlugin(AMIPlugin):
    name = 'sfcb-client-setup'
    _sectionName = 'sfcb-client-setup'

    def configure(self):
        cfg = self.ud.getSection(self._sectionName)
        if not cfg:
            return

        # Get the cert name
        certHashField = 'x509-cert-hash'
        certField = 'x509-cert(base64)'
        if certHashField not in cfg or certField not in cfg:
            return

        x509CertHash = cfg[certHashField]
        if not x509CertHash.endswith('.0'):
            x509CertHash += '.0'
        x509Cert = cfg[certField]
        try:
            x509Cert = base64.decodestring(x509Cert)
        except:
            # Malformed base64 data. We ignore it.
            return
        sfcbConfigDir = self.getSfcbConfigDir()
        if sfcbConfigDir is None:
            return
        certsDir = os.path.join(sfcbConfigDir, "clients")
        certsFileName = os.path.join(certsDir, os.path.basename(x509CertHash))
        # Exceptions are properly displayed by ami.py
        util.mkdirChain(certsDir)
        file(certsFileName, "w").write(x509Cert)

    def getSfcbConfigDir(self):
        configDirs = [
            os.path.join(os.sep, self.id.rootDir, "etc", "conary", "sfcb"),
            os.path.join(os.sep, self.id.rootDir, "etc", "sfcb"),
        ]
        for configDir in configDirs:
            if not os.path.isdir(configDir):
                continue
            cfgFilePath = os.path.join(configDir, "sfcb.cfg")
            if os.path.isfile(cfgFilePath):
                return configDir
        return None
