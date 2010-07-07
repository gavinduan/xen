# $Id: plugin_virtual_host.py,v 1.4 2010/07/07 23:18:39 bruno Exp $
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
# $Log: plugin_virtual_host.py,v $
# Revision 1.4  2010/07/07 23:18:39  bruno
# added 'power on + install' command
#
# Revision 1.3  2010/06/30 17:59:58  bruno
# can now route error messages back to the terminal that issued the command.
#
# can optionally set the VNC viewer flags.
#
# Revision 1.2  2010/06/23 22:23:37  bruno
# fixes
#
# Revision 1.1  2010/06/22 21:41:14  bruno
# basic control of VMs from within a VM
#
#

import rocks.commands
import rocks.vm
import sys

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'virtual-host'

	def run(self, args):
		host = args[0]
		state = args[1]
		key = args[2]

		if not key:
			print 'need to supply a private key'
			sys.exit(-1)
			
		#
		# if 'vm-controller' is set, then we assume this is a virtual
		# frontend and we want to send a command to the VM controller
		# for this virtual cluster.
		#
		vm_controller = self.db.getHostAttr('localhost',
			'vm-controller')
		if vm_controller:
			vm = rocks.vm.VMControl(self.db, vm_controller, key)

			if state == 'on':
				op = 'power on'
			elif state == 'off':
				op = 'power off'
			elif state == 'on+install':
				op = 'power on + install'

			(status, reason) = vm.cmd(op, host)

			if status != 0:
				print 'command failed\n%s' % reason
				sys.exit(-1)

