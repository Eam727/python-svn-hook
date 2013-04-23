#! /usr/bin/env python
# -*- coding: utf-8 -*- 
"""
SVN�ύǰ��鹳��
���ܣ�
	1��ǿ����д�ύע�ͣ�����10�ֽ�����
	2��ǿ��ע�͸�ʽΪ��xxx:xxx
	3���ύ�ļ���飬���˲������ύ���ļ�

����: ��˼�� <lsj86@qq.com> <2012/04/28>
"""

import sys
import os
import re

def main(argv):
	(repos, txn) = argv
	badlist = (".*config\.php$", ".*/php/cache", ".*test", "config\.js$","^.*\.db$")
	message = "".join(os.popen("/usr/bin/svnlook log '%s' -t '%s'" % (repos, txn)).readlines()).strip()
	if len(message) < 10:
		sys.stderr.write("�����뱾���ύ���޸����ݣ�10�ֽ����ϡ�");
		sys.exit(1)
	if message.find(':') < 1:
		sys.stderr.write("�밴�淶��дע�ͣ���ʽΪ��������: �޸�˵����");
		sys.exit(1)

	changelist = os.popen("/usr/bin/svnlook changed '%s' -t '%s'" % (repos, txn)).readlines()
	for line in changelist:
		for pattern in badlist:
			if re.search(pattern, line):
				sys.stderr.write("�벻Ҫ�� %s ����汾�⡣" % line[1:].strip());
				sys.exit(1)
	sys.exit(0)

if __name__ == "__main__":
	main(sys.argv[1:])