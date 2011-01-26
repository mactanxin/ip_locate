# -*- coding: utf-8 -*-
# encoding: utf-8

import sys

class progressBar:
    def __init__(self, minValue = 0, maxValue = 100, totalWidth=80):
        """初始化
        """
        self.bar = "[]"   # 进度条字符串
        self.min = minValue
        self.max = maxValue
        self.span = maxValue - minValue
        self.width = totalWidth
        self.amount = 0       # 进度值。
        self.update(0)  # 构造初始进度条字符串
 
    def update(self, newAmount = 0):
        """ 用新数值更新进度条。
            如果数值参数在最大值/最小值范围以外，则显示最大值/最小值。
        """
        if newAmount < self.min: newAmount = self.min
        if newAmount > self.max: newAmount = self.max
        self.amount = newAmount
 
        # 计算新的进度百分比，取整。
        diffFromMin = float(self.amount - self.min)
        percentDone = (diffFromMin / float(self.span)) * 100.0
        percentDone = int(round(percentDone))
 
        # 计算显示某个进度所需要的条块
        allFull = self.width - 2
        numHashes = (percentDone / 100.0) * allFull
        numHashes = int(round(numHashes))
 
        # 用'='和'>'号构造进度条字符串,对空和满格进行特殊处理
        if numHashes == 0:
            self.bar = "[>%s]" % (' '*(allFull-1))
        elif numHashes == allFull:
            self.bar = "[%s]" % ('='*allFull)
        else:
            self.bar = "[%s>%s]" % ('='*(numHashes-1),
                                        ' '*(allFull-numHashes))
 
        # 计算百分比显示位置，基本位于中央 
        percentPlace = (len(self.bar) / 2) - len(str(percentDone))
        percentString = str(percentDone) + "%"
 
        # 把百分比插入进度条
        self.bar = ''.join([self.bar[0:percentPlace], percentString,
                                self.bar[percentPlace+len(percentString):]
                                ])
 
    def __str__(self):
        return str(self.bar)
 
    def __call__(self, value):
        """ 更新进度数字，显示进度条。先输出一个回车，使显示能够覆盖当前行。
        """
        print '\r',
        self.update(value)
        sys.stdout.write(str(self))
        sys.stdout.flush()