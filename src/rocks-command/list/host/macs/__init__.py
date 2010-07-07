# $Id: __init__.py,v 1.3 2010/07/07 23:18:39 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: __init__.py,v $
# Revision 1.3  2010/07/07 23:18:39  bruno
# added 'power on + install' command
#
# Revision 1.2  2010/06/30 17:59:58  bruno
# can now route error messages back to the terminal that issued the command.
#
# can optionally set the VNC viewer flags.
#
# Revision 1.1  2010/06/28 17:22:56  bruno
# added 'list host macs' command
#
#

import rocks.commands
import rocks.vm

class command(rocks.commands.HostArgumentProcessor,
	rocks.commands.list.command):

	MustBeRoot = 0


class Command(command):
	"""
	Get a list of MAC addresses for all the hosts that are associated
	with a virtual cluster.

	<arg type='string' name='host'>
	Host name of machine. This host name should be the name of the
	virtual frontend for the virtual cluster that you want the MAC
	addresses for.
	</arg>

	<param type='string' name='key'>
	A private key that will be used to authenticate the request. This
	should be a file name that contains the private key.
	</param>
	"""

	def run(self, params, args):
		key, = self.fillParams([ ('key', ) ])

		if not key:
			self.abort('must supply a path name to a private key')

		vm_controller = self.db.getHostAttr('localhost',
			'vm-controller')

		if not vm_controller:
			self.abort('the "vm-controller" attribute is not set')

		if len(args) == 0:
			self.abort('must supply one host name')
		if len(args) > 1:
			self.abort('must supply only one host name')

		hosts = self.getHostnames(args)
		host = hosts[0]

		vm = rocks.vm.VMControl(self.db, vm_controller, key)
		(status, macs) = vm.cmd('list macs', host)
		if status != 0:
			self.abort('command failed: %s' % macs)

		self.beginOutput()
		for mac in macs.split('\n'):
			if len(mac) > 0:
				self.addOutput('', (mac))
		self.endOutput(header=['', 'macs in cluster'])

