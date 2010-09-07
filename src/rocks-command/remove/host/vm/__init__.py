# $Id: __init__.py,v 1.11 2010/09/07 23:53:33 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4 (Maverick)
# 
# Copyright (c) 2000 - 2010 The Regents of the University of California.
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
# Revision 1.11  2010/09/07 23:53:33  bruno
# star power for gb
#
# Revision 1.10  2009/05/01 19:07:34  mjk
# chimi con queso
#
# Revision 1.9  2008/10/18 00:56:23  mjk
# copyright 5.1
#
# Revision 1.8  2008/09/02 18:19:29  phil
# Plugin to also remove any host-specific bootprofiles when removing vm host
#
# Revision 1.7  2008/09/02 18:03:16  phil
# support plugin to remove host-specific bootprofile when removing vm host
#
# Revision 1.6  2008/04/21 16:37:35  bruno
# nuked the vm_macs table -- now using the networks table to store/retrieve
# mac addresses for VMs
#
# Revision 1.5  2008/04/17 16:38:21  bruno
# incorporate phil's vm changes
#
# Revision 1.4  2008/03/06 23:42:04  mjk
# copyright storm on
#
# Revision 1.3  2008/02/01 21:38:54  bruno
# closer
#
# Revision 1.2  2008/02/01 21:27:53  bruno
# plugin for removing VM configuration info from the database
#
# Revision 1.1  2007/12/03 19:48:51  bruno
# xen for V
#
#

import os
import rocks.commands

class Command(rocks.commands.remove.host.command):
	"""
	Remove the configuration info in the database for the supplied hosts.

	<arg type='string' name='host' repeat='1'>
	A list of one or more VM host names.
	</arg>

	<example cmd='remove host vm compute-0-0-0'>
	Remove the configuration info in the database for compute-0-0-0.
	</example>
	"""

	def run(self, params, args):
		if not len(args):
			self.abort('must supply at least one host')
			
		for host in self.getHostnames(args):
                	self.runPlugins(host)
			vmnodeid = None
			mem = None
			cpus = None
			macs = None
			disks = None

			#
			# get the node id of the VM
			#
			rows = self.db.execute("""select vn.id from
				nodes n, vm_nodes vn where vn.node = n.id
				and n.name = '%s' """ % host)
			
			if rows != 1:
				continue

			vmnodeid, = self.db.fetchone()

			if not vmnodeid:
				continue

			#
			# get the name of the physical node that hosts
			# this VM
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

			#
			# remove the configuration file on the physical node
			#
			os.system('ssh -q %s "rm -f /etc/xen/rocks/%s"' % 
				(physhost, host))

			#
			# now remove the relevant rows in the database for
			# this VM
			#
			self.db.execute("""delete from vm_nodes where
				id = %s""" % (vmnodeid))

			self.db.execute("""delete from vm_disks where
				vm_node = %s""" % (vmnodeid))

