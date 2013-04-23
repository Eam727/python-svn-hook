#! /usr/bin/env python
# -*- coding: utf-8 -*- 
"""
SVN�ύ������
����˵��: 
	������Ա�ύ�ļ���SVN��SVN��ִ�иù��ӳ��򣬸ó����𽫸��µ��ļ�������webĿ¼�£�ʵ���Զ�����

����: ��˼�� <lsj86@qq.com> <2012/04/28>
"""
import os
import sys
import shutil

reload(sys)
sys.setdefaultencoding('utf-8')

def main(argv):
	'''
	+======================================================
	+ ʹ�÷���: post-commit /data/svn/test 11
	+ SVN���ù���ʱ�ᴫ2��������1:SVN�ֿ�·�� 2:��ǰ�汾��
	+======================================================
	'''
	(repos, txn) = argv
	servers = {}
	servers["zh_CN"] = ("trunk", "/data/www/zh_CN", "/data/svnupdate/zh_CN")
	servers["zh_TW"] = ("branches/zh_TW", "/data/www/zh_TW", "/data/svnupdate/zh_TW")

	logs = []
	
	svninfo = os.popen("/usr/bin/svnlook info '%s'" % repos).readlines()
	logs.append("�ύ��: %s\r\n�ύʱ��: %s\r\n��ǰ�汾: %s\r\n�ύ˵��: %s" % (svninfo[0], svninfo[1], svninfo[2], svninfo[3]))
	logs.append("===============================================")

	logs.append("\r\n�ı��ļ��б�: ")
	changelist = os.popen("/usr/bin/svnlook changed '%s'" % repos).readlines()
	logs.append("/usr/bin/svnlook changed '%s'" % repos)
	logs.append("".join(changelist))
	
	logs.append("\r\n�ı�Ŀ¼�б�: ")
	changedirs = os.popen("/usr/bin/svnlook dirs-changed %s" % repos).readlines()
	logs.append("/usr/bin/svnlook dirs-changed %s" % repos)
	logs.append("".join(changedirs))
	
	logs.append("\r\nִ��svnupdate�汾����: ")
	version = ''
	for d in changedirs:
		if version == '':
			for k, v in servers.items():
				if len(d) > len(v[0]) and d[:len(v[0])] == v[0]:
					version = k
					offset  = len(v[0])
					break
		if version == '':
			return
		os.system("/usr/bin/svn update %s%s" % (servers[version][2], d[offset:]))
		logs.append("/usr/bin/svn update %s%s" % (servers[version][2], d[offset:]))

	logs.append("\r\n���ļ�������WEBĿ¼:")
	
	for line in changelist:
		op   = line[:1]
		line = line[1:].strip()[offset:]
		src  = servers[version][2] + line
		dst  = servers[version][1] + line
		
		if op == "D": #ɾ���ļ�
			os.system("rm -f %s" % dst);
			logs.append("rm -f %s" % dst)
			continue
		if op == "A": #�����ļ�
			if not os.path.exists(os.path.dirname(dst)):
				os.system("mkdir -p %s" % os.path.dirname(dst))
				logs.append("mkdir -p %s" % os.path.dirname(dst))
		if os.path.isfile(src):
			os.system("cp -f %s %s" % (src, dst))
			logs.append("cp -f %s %s" % (src, dst))
	
	logs.append("\r\n")
	fp = open("/data/www/logs/%s_%s.log" % (version, txn), "wb")
	fp.write("\r\n".join(logs))
	fp.close()

	print "ȫ��������ɣ���ϸ��Ϣ��鿴: /data/www/logs/%s_%s.log" % (version, txn)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print main.__doc__
	else:
		main(sys.argv[1:])