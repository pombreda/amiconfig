#
# Copyright (c) 2007-2008 rPath, Inc.
#

import urllib
import urlparse

from amiconfig.errors import *
from amiconfig.plugin import AMIPlugin

class AMIConfigPlugin(AMIPlugin):
    name = 'noip'

    def configure(self):
        try:
            self.cfg = self.ud.getSection('noip')
        except EC2DataRetrievalError:
            return

        for key in ('username', 'password'):
            if key not in self.cfg:
                return

        template = True
        for key in ('prefix', 'domain', 'start'):
            if key not in self.cfg:
                template = False
                break

        if not template and 'hostname' not in self.cfg:
            return

        if template:
            index = int(self.id.getAMILaunchIndex())
            start = int(self.cfg['start'])
            id = '%02d' % (start + index)
            self.cfg['hostname'] = '%s.%s' % (id, self.cfg['domain'])

        url = ('https://%(username)s:%(password)s@dynupdate.no-ip.com'
               '/nic/update?hostname=%(hostname)s') % self.cfg

        urlfh = urllib.urlopen(url)

        ret = urlfh.read()
