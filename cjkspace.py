#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cjkspace - Insert '~' or other symbols between CJK and Western characters.
# http://gosman.blogbus.com
#
# Copyright 2007 连明昌(gosman)
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, version 2.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You have received a copy of the GNU General Public License along
#   with this program, on the COPYING file.
#
#============================================================================= 
# This file default use UTF-8 encoding.
import re,getopt,string,sys,os,shutil

VERSION = '0.1'
mylink = "http://gosman.blogbus.com"

#====================================== Edit Area ===========================================
# If you want to change or add the Range or Verbatim keyword,you can change in here.
# More information see the help file cjkspace.pdf
#
# Reference http://blog.oasisfeng.com/2006/10/19/full-cjk-unicode-range/
# http://www.unicode.org
CJK_Range = [[u'\u3400',u'\u4db5'],
		[u'\u4e00',u'\u9fa5'],
		[u'\u9fa6',u'\u9fbb'],
		[u'\uf900',u'\ufa2d'],
		[u'\ufa30',u'\ufa6a'],
		[u'\ufa70',u'\ufad9'],
		[u'\u20000',u'\u2a6d6'],
		[u'\u2f800',u'\u2fa1d']]
Letter_Range = [[u'A',u'Z'],
		[u'a',u'z'],
		[u'0',u'9']]
Verbatim_Str = ['verbatim','Verbatim','comment']
#===========================================================================================
# Supported Encoding
encoding_str = "ascii 646 us-ascii big5	big5-tw csbig5 big5hkscs big5-hkscs hkscs cp037	IBM037 IBM039 cp424 EBCDIC-CP-HE IBM424 cp437 437 IBM437 cp500 EBCDIC-CP-BE EBCDIC-CP-CH IBM500 cp737 cp775 IBM775 cp850 850 IBM850 cp852 852 IBM852 cp855 855 IBM855 cp856 cp857 857 IBM857 cp860 860 IBM860 cp861 861 CP-IS IBM861 cp862 862 IBM862 cp863 863 IBM863 cp864 IBM864 cp865 865 IBM865 cp866 866 IBM866 cp869 869 CP-GR IBM869 cp874 cp875 cp932 932 ms932 mskanji ms-kanji cp949 949 ms949 uhc cp950 950 ms950 cp1006 cp1026 ibm1026 cp1140 ibm1140 cp1250 windows-1250 cp1251 windows-1251 cp1252 windows-1252 cp1253 windows-1253 cp1254 windows-1254 cp1255 windows-1255 cp1256 windows1256 cp1257 windows-1257 cp1258 windows-1258 euc_jp eucjp ujis u-jis euc_jis_2004 jisx0213 eucjis2004 euc_jisx0213 eucjisx0213 euc_kr euckr korean ksc5601 ks_c-5601 ks_c-5601-1987 ksx1001 ks_x-1001 gb2312 chinese csiso58gb231280 euc-cn euccn eucgb2312-cn gb2312-1980 gb2312-80 iso-ir-58 gbk 936 cp936 ms936 gb18030 gb18030-2000 hz hzgb hz-gb hz-gb-2312 iso2022_jp csiso2022jp iso2022jp iso-2022-jp iso2022_jp_1 iso2022jp-1 iso-2022-jp-1 iso2022_jp_2 iso2022jp-2 iso-2022-jp-2 iso2022_jp_2004 iso2022jp-2004 iso-2022-jp-2004 iso2022_jp_3 iso2022jp-3 iso-2022-jp-3 iso2022_jp_ext iso2022jp-ext iso-2022-jp-ext iso2022_kr csiso2022kr iso2022kr iso-2022-kr latin_1 iso-8859-1 iso8859-1 8859 cp819 latin latin1 L1 iso8859_2 iso-8859-2 latin2 L2 iso8859_3 iso-8859-3 latin3 L3 iso8859_4 iso-8859-4 latin4 L4 iso8859_5 iso-8859-5 cyrillic iso8859_6 iso-8859-6 arabic iso8859_7 iso-8859-7 greek greek8 iso8859_8 iso-8859-8 hebrew iso8859_9 iso-8859-9 latin5 L5 iso8859_10 iso-8859-10 latin6 L6 iso8859_13 iso-8859-13 iso8859_14 iso-8859-14 latin8 L8 iso8859_15 iso-8859-15 johab cp1361 ms1361 koi8_r koi8_u mac_cyrillic maccyrillic mac_greek 	macgreek mac_iceland maciceland mac_latin2 maclatin2 maccentraleurope mac_roman macroman mac_turkish macturkish ptcp154 csptcp154 pt154 cp154 cyrillic-asian shift_jis csshiftjis shiftjis sjis s_jis shift_jis_2004 shiftjis2004 sjis_2004 sjis2004 shift_jisx0213 shiftjisx0213 sjisx0213 s_jisx0213 utf_16 U16 utf16 utf_16_be UTF-16BE utf_16_le UTF-16LE utf_7 U7 unicode-1-1-utf-7 utf_8 U8 UTF utf8 utf_8_sig"	
# verbatim的正则表达式
re_verb_begin = re.compile(r'((^[ \t]*)\\begin(\[.*\])*\{(.*)\}(\[.*\])*)')
re_verb_end = re.compile(r'((^[ \t]*)\\end(\[.*\])*\{(.*)\}(\[.*\])*)')

def isCJK(char):
	for range in CJK_Range:
		if (char >= range[0]) and (char <= range[1]):
			return True
	return False

def isletter(char):
	for range in Letter_Range:
		if (char >= range[0]) and (char <= range[1]):
			return True
	return False

def insert():
	global infile_path,outfile_path,one_file
	#if is_encode:
	#	iconv_cmd="iconv -f " + encoding + " -t UTF-8 " + infile_path + " --output " + infile_path + ".tmp"
	#	os.system(iconv_cmd)
	#	infile_path = infile_path + ".tmp"
	no_verb = True
	no_comment = True
	try:
		infile = open(infile_path,'r')
	except IOError:
		print "Open File Error!"
		sys.exit(4)
	pre = u'\u0000'
	cur = u'\u0000'
	seek_cnt = 0
	blank = False
	latexcmd = False
	pre_blank_CJK = False
	pre_blank_letter = False
	is_blank_insert = False
	line_list = infile.readlines()
	infile.close()
	outfile = os.tmpfile()
	for line in line_list:
		# 逃脱Verbatim模式
		re_verb_str = re_verb_begin.search(line)
		if re_verb_str:
			verb_str = re_verb_str.groups()[3] # 取出{}中字符串,如verbatim
			if verb_str in Verbatim_Str:
				no_verb = False
		re_verb_str = re_verb_end.search(line)
		if re_verb_str:
			verb_str = re_verb_str.groups()[3] # 取出{}中字符串
			if verb_str in Verbatim_Str:
				no_verb = True
		try:
			line_uni = unicode(line,encoding)
		except UnicodeDecodeError:
			sys.stderr.write("Please specify correct encoding,try '-e' or '--encoding' option.\nExit Error!\n")
			sys.exit(1)
		for str_uni in line_uni:
			cur = str_uni
			if (cur == u'%') and (pre != u'\\'):
				# 开始注释
				no_comment = False 
			if all:
				no_verb = True
				no_comment = True
				latexcmd = False
			if no_verb and no_comment and (not latexcmd):
				# 不在Verbatim, 注释里才处理
				# 删除多余的空格
				if (cur == u'\\'):
					latexcmd = True
				if (isCJK(pre) or isletter(pre)) and (cur == u' '):
					pre_blank_CJK = isCJK(pre)
					pre_blank_letter = isletter(pre)
					seek_cnt = 0 # 事后清零，不如初始时赋值
					blank = True
				if blank and (cur == u' '):
					seek_cnt = seek_cnt - 1
				else:
					# 已经不是空格
					if (isCJK(cur) and pre_blank_letter) or (isletter(cur) and pre_blank_CJK):
						outfile.seek(seek_cnt,1)
						is_blank_insert = True # 在删除多余空格，添加字符
					pre_blank_CJK = False
					pre_blank_letter = False
					
				# 插入字符
				if (isCJK(cur) and isletter(pre)) or (isCJK(pre) and isletter(cur)) or is_blank_insert:
					is_blank_insert = False
					outfile.write(token)
			# latex命令结束
			if (not cur.isalpha() and cur != u'\\'):
				latexcmd = False
			outfile.write(cur.encode(encoding))
			pre = str_uni
		no_comment = True
	outfile.seek(0)
	output_str = outfile.read()
	if std_out:
		sys.stdout.write(output_str)
	else:
		try:
			output_file = open(outfile_path,'w')
		except IOError:
			print "Open File Error!"
			sys.exit(4)
		output_file.write(output_str)
		output_file.close()
	outfile.close()
def main():
	global token,one_file,backup,encoding 
	global infile_path,outfile_path,std_out,Verbatim_Str
	global all
	all = False
	std_out = True
	infile_path = ''
	outfile_path = ''
	backup = True
	cover = False
	encoding = 'utf8'
	output = False
	token = '~'
	try:
		opts,args = getopt.getopt(sys.argv[1:],"Vhd:e:o:cnv:lx:a",["version","help",
								"delimeter=","encoding=",
								"output=","cover","nobackup",
								"verbatim=","list",
								"noverbatim=","all"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt,arg in opts:
		if opt in ("-h","--help"):
			usage()
			sys.exit(0)
		elif opt in ('-d',"--delimeter"):
			token = arg
		elif opt in ('-e',"--encoding"):
			encoding = arg
		elif opt in ('-o',"--output"):
			output = True
			std_out = False
			outfile_path = arg
		elif opt in ('-c',"--cover"):
			cover = True
			std_out = False
		elif opt in ('-n',"--nobackup"):
			backup = False
		elif opt in ('-a',"--all"):
			all = True
		elif opt in ('-v',"--verbatim"):
			Verbatim_Str = Verbatim_Str + arg.split()
		elif opt in ('-x',"--noverbatim"):
			for no_verbatim_str in arg.split():
				try:
					index = Verbatim_Str.index(no_verbatim_str)
				except ValueError:
					sys.stderr.write('Warning: "' + no_verbatim_str + '"' + 'enviroment no defined!\n')
					continue
				del Verbatim_Str[index]
		elif opt in ('-l',"--list"):
			print "The following list contain all the coded character sets known.One coded character set can be listed with several different names (aliases).\n\n" + encoding_str
			sys.exit(0)
		elif opt in ('-V','--version'):
			print "cjkspace %s \nCopyright (C) 2007 Gosman Lian.\nThis is free software; see the source for copying conditions.  There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\nWritten by Gosman Lian." % VERSION 
			sys.exit(0)
		else:
			usage()
			sys.exit(1)
	if len(args) > 1:
		# 多输入处理
		std_out = False
		for infile_path in args:
			if cover:
				outfile_path = infile_path
				if backup:
					shutil.copyfile(infile_path,infile_path + ".bak")
			else:
				outfile_path = infile_path + '.out'
			insert()
		if output:
			print "Waring: You input multiple files, now you should not specify '-o' or '--output' options."
	elif len(args) == 1:
		infile_path = args[0]
		if cover:
			outfile_path = infile_path
			if backup:
				shutil.copyfile(infile_path,infile_path + ".bak")
		insert()
	else:
		usage()
		sys.exit(1)

def usage():
	USAGE = string.join(["Usage: cjkspace [options] [inputfile]\nInsert '~' or other symbols between CJK and Western characters.\n\n",
		"Options:\n",
		" -d, --delimeter delimeter	inserting specify delemeter instead of '~'\n",
		" -n, --nobackup		no backup your original file\n",
		" -o, --output filename		specify your output filename\n",
		" -c, --cover 			output files will cover your original files,default will be backuped\n",
		" -a, --all			inserting delimeter in everywhere, not considering comment, verbatim etc.\n",
		" -v, --verbatim verbatim	add the verbatim like enviroment\n",
		" -x, --noverbatim verbatim	del the verbatim like enviroment form the list\n",
		" -e, --encoding encoding	specify your file's encoding if not utf-8\n",
		" -l, --list			list all known coded character sets\n",
		" -h, --help			display this help information\n",
		" -V, --version			print program version\nFor more information or bug reporting,please see:\n<%s>" % mylink])
	print USAGE

if __name__ == '__main__':
	main()
	sys.exit(0)
