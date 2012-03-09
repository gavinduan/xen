# $Id: __init__.py,v 1.11 2012/03/09 01:45:24 clem Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4.3 (Viper)
# 
# Copyright (c) 2000 - 2011 The Regents of the University of California.
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
# 	Development Team at the San Diego Supercomputer Center at the
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
# Revision 1.11  2012/03/09 01:45:24  clem
# Rocks command xen is not compatible with 5.7 and 6.2
#
# Revision 1.10  2011/07/23 02:31:46  phil
# Viper Copyright
#
# Revision 1.9  2010/09/07 23:53:34  bruno
# star power for gb
#
# Revision 1.8  2009/12/01 18:54:41  bruno
# suppress error message when trying to stop a VM that is isn't running.
#
# Revision 1.7  2009/05/01 19:07:35  mjk
# chimi con queso
#
# Revision 1.6  2009/04/14 17:41:37  bruno
# bug fix
#
# Revision 1.5  2009/04/08 22:27:59  bruno
# retool the xen commands to use libvirt
#
# Revision 1.4  2008/10/18 00:56:24  mjk
# copyright 5.1
#
# Revision 1.3  2008/05/05 22:04:11  bruno
# doc fix
#
# Revision 1.2  2008/03/06 23:42:05  mjk
# copyright storm on
#
# Revision 1.1  2008/01/30 22:01:35  bruno
# closer
#
#

import os
import tempfile
import rocks.commands

import sys
sys.path.append('/usr/lib64/python2.' + str(sys.version_info[1]) + '/site-packages')
sys.path.append('/usr/lib/python2.' + str(sys.version_info[1]) + '/site-packages')
import libvirt

#
# this function is used to suppress an error message when we start a VM
# for the very first time and there isn't a disk file created for it yet.
# the error message looks like:
#
#	libvirt.libvirtError: Domain not found: xenUnifiedDomainLookupByName
#
def handler(ctxt, err):
	global errno

	errno = err


class Command(rocks.commands.stop.host.command):
	"""
	Destroy a VM slice on a physical node.

	<arg type='string' name='host' repeat='1'>
	A list of one or more VM host names.
	</arg>

	<example cmd='stop host vm compute-0-0-0'>
	Stop VM host compute-0-0-0. This is equivalent to a 'hard power off',
	(i.e., pulling the power cord from a node).
	</example>
	"""

	def run(self, params, args):
		hosts = self.getHostnames(args)
		
		if len(hosts) < 1:
			self.abort('must supply host')

		for host in hosts:
			#
			# the name of the physical host that will boot
			# this VM host
			#
			rows = self.db.execute("""select vn.physnode from
				vm_nodes vn, nodes n where n.name = '%s'
				and n.id = vn.node""" % (host))

			if rows == 1:
				physnodeid, = self.db.fetchone()
			else:
				continue

			rows = self.db.execute("""select name from nodes where
				id = %s""" % (physnodeid))

			if rows == 1:
				physhost, = self.db.fetchone()
			else:
				continue

			hipervisor = libvirt.open('xen://%s/' % physhost)
			libvirt.registerErrorHandler(handler, 'context')

			try:
				domU = hipervisor.lookupByName(host)
				domU.destroy()
			except:
				pass

