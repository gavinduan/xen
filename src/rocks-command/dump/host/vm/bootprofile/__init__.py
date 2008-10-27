# $Id: __init__.py,v 1.1 2008/10/27 20:15:19 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		           version 5.1  (VI)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
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
# Revision 1.1  2008/10/27 20:15:19  bruno
# dump host-specific bootprofile info
#
#

import os
import sys
import string
import rocks.commands

class Command(rocks.commands.dump.host.command):
	"""
	Dump host VM boot profile information as Rocks commands.
		
	<arg optional='1' type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied, 
	information for all hosts will be listed.
	</arg>

	<example cmd='dump host vm bootprofile compute-0-0-0'>
	Dump VM boot profile for compute-0-0-0.
	</example>

	<example cmd='dump host vm'>
	Dump VM boot profile for all configured virtual machines.
	</example>
		
	<related>add host vm</related>
	"""

	def dumpVM(self, host):
		rows = self.db.execute("""select vp.vm_node
			from vm_profiles vp, vm_nodes vn, nodes n where
			vp.vm_node = vn.id and vn.node = n.id and
			n.name = '%s'""" % host)

		if rows == 0:
			return

		vmnodeid, = self.db.fetchone()

		rows = self.db.execute("""select profile, kernel, ramdisk, args
			from vm_profiles where vm_node = %s""" % (vmnodeid))

		if rows == 0:
			return

		for (profile, kernel, ramdisk, args) in self.db.fetchall():
			str = "add host vm bootprofile %s" % host

			if profile:
				str += " profile='%s'" % (profile)
			if kernel:
				str += " kernel='%s'" % (kernel)
			if ramdisk:
				str += " ramdisk='%s'" % (ramdisk)
			if args:
				str += " args='%s'" % (args)

			self.dump(str)


	def run(self, params, args):
		for host in self.getHostnames(args):
			self.dumpVM(host)

