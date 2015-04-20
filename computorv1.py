#!/usr/bin/python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#                                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/04/20 15:46:41 by jaguillo          #+#    #+#              #
#    Updated: 2015/04/20 17:21:13 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sys import argv
from re import compile

# 5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0
# 4 * X^0 + 4 * X^1 - 9.3 * X^2 = 0
# 5 * X^0 + 4 * X^1 = 4 * X^0
# 1 * X^0 + 4 * X^1 = 0
# 8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0
# 5 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 0
# 5 + 4 * X + X^2= X^2

class Polynom():

	sign = None
	num = 0
	x = False
	power = 0

	def __init__(self, m, sign = None, num = 0, x = False, power = 0):
		self.sign = sign
		self.num = num
		self.x = x
		self.power = power
		if m == None:
			return
		if len(m.group(1)) > 0:
			self.sign = m.group(1)
			if self.sign == '=':
				raise
		if m.group(2) == None:
			self.num = 1.0
		else:
			self.num = float(m.group(2))
		if m.group(3) != None:
			self.x = True
			if m.group(4) != None:
				self.power = int(m.group(4))

	def toString(self):
		s = ""
		if self.sign != None:
			s += self.sign
			s += " "
		if self.x and self.num == 1:
			s += "X^%d" % (self.power)
		elif self.x:
			s += "(%s * X^%d)" % (str(self.num), self.power)
		else:
			s += str(self.num)
		return s


reg_polynom = compile('([-+=]?)\s*([0-9\.]+)?(\s*\*?\s*[xX](?:\^([0-9]+))?)?\s*')
reg_space = compile('\s+')

class Computer():

	left = []
	right = []
	eq = None

	def __init__(self, equation):
		self.left = []
		self.right = []
		self.eq = equation

	def parse(self):
		pos = 0
		left = True
		while pos < len(self.eq):
			if self.eq[pos:pos+1] == "=" and left and len(self.left) > 0:
				left = False
				pos += 1
			m = reg_space.match(self.eq, pos)
			if m != None:
				pos += len(m.group(0))
				continue
			m = reg_polynom.match(self.eq, pos)
			if m == None or len(m.group(0)) <= 0:
				print("Unexpected syntax: '%s'" % (self.eq[pos:]))
				return False
			try:
				p = Polynom(m)
			except:
				print("Invalid syntax: '%s'" % (self.eq[pos:]))
				return False
			if left:
				self.left.append(p)
			else:
				self.right.append(p)
			pos += len(m.group(0))
		if len(self.left) == 0:
			if len(self.right) == 0:
				print("Bad argument")
				return False
			self.left.append(Polynom(None))
		if len(self.right) == 0:
			self.right.append(Polynom(None))
		s = "Parsing -> "
		for p in self.left:
			s += p.toString()
			s += " "
		s += "="
		for p in self.right:
			s += " "
			s += p.toString()
		print(s)
		return True

	def reduce(self):
		return False

	def resolve(self):
		return False


if len(argv) <= 1:
	print("Not enougth argument")
else:
	c = Computer(argv[1])
	if not c.parse():
		exit(1)
	if not c.reduce():
		exit(1)
	if not c.resolve():
		exit(1)

