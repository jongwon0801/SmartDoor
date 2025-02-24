# /home/pi/www/python/elcsoft/components.py

#!/usr/bin/python

import sys
import lib
import elcsoft.db

from decimal import *
from pydoc import describe

class Components(object):
    __lib__ = {}
    
    def __init__(self):
        global global_config
        if not 'global_config' in globals():
            global_config = lib.getConfigByJsonFile('/home/pi/www/python/config.json')

        self.__lib__['db'] = global_config['db']
        self.__lib__['conn'] = elcsoft.db.DBConn(**self.__lib__['db'])
        
        self.__tableName__ = ''
        self.__fields__ = {}
        self.__labels__ = []
        self.__conditions__ = []
        self.__orderby__ = []
        self.__groupby__ = []
        
        self.__formName__ = 'listForm'
        self.__action__ = ''
        self.__buttons__ = []
        self.__searchFields__ = []
        self.isCart = True
        
        self.keyword = ''
        self.page = 1
        self.rowsPerPage = 20
        self.showPageNum = 10
        
        self.total = 0
        self.totalPages = 0
        self.start = 0
        self.results = None
        self.data = []
        
         
    # setField
    def setField(self, name, value) :
        self.__fields__[name] = value
    
    # setField
    def setFieldByColumns(self, columns, label='') :
        for column in columns :
            key = column['field']
            if label == '':
                name = key
                value = key
            else :
                name = label + '.' + key 
                value = label + '_' + key 
            self.setField(name, value)

    # setJoin
    def setJoin(self, className, label='', condition=''):
        moduleName = ''
        for i in range(len(className)) :
            if className[i].isupper() :
                if i == 0 :
                    moduleName = moduleName + className[i].lower()
                else :
                    moduleName = moduleName + "_" + className[i].lower()
            else :
                moduleName = moduleName + className[i]
        moduleName = "elcsoft.model." + moduleName
        
        module = __import__(moduleName, fromlist=className)
        obj = getattr(module, className)()
        
        if self.__tableName__ != '' :
            self.__tableName__ = self.__tableName__ + ' JOIN '
        
        self.__tableName__ = self.__tableName__ + obj.__tableName__
        
        if label != '' :
            self.__tableName__ = self.__tableName__ + ' AS ' + label
            
        self.setFieldByColumns(obj.__column__, label)
        
        if condition != '':
            self.setAndCondition(condition)
    
    # setLeftOuterJoin
    def setLeftOuterJoin(self, className, label='', condition=''):
        moduleName = ''
        for i in range(len(className)) :
            if className[i].isupper() :
                if i == 0 :
                    moduleName = moduleName + className[i].lower()
                else :
                    moduleName = moduleName + "_" + className[i].lower()
            else :
                moduleName = moduleName + className[i]
        moduleName = "elcsoft.model." + moduleName
        
        module = __import__(moduleName, fromlist=className)
        obj = getattr(module, className)()
        
        if self.__tableName__ != '' :
            self.__tableName__ = self.__tableName__ + ' LEFT OUTER JOIN '
        
        self.__tableName__ = self.__tableName__ + obj.__tableName__
        
        if label != '' :
            self.__tableName__ = self.__tableName__ + ' AS ' + label

        if condition != '':
            self.__tableName__ = self.__tableName__ + ' ON ' + condition
            
        self.setFieldByColumns(obj.__column__, label)
            
    # setLabel
    def setLabel(self, index, name, value):
        data = {}
        data[name] = value
        
        if not index in self.__labels__ :
            self.__labels__.insert(index, [])
        
        self.__labels__[index].append(data)
            
    # setButton
    def setButton(self, **kwargs):
        if 'name' in kwargs :
            self.__buttons__.append(kwargs)

    # setCondition
    def setCondition(self, **kwargs):
        if 'condition' in kwargs :
            self.__conditions__.append(kwargs)
            
    # setAndCondition
    def setAndCondition(self, condition):
         self.setCondition(type='AND',condition=condition)
            
    # setOrCondition
    def setOrCondition(self, condition):
         self.setCondition(type='OR',condition=condition)
    
    # setSort
    def setSort(self, sort, desc):
        data = {}
        data['sort'] = sort
        data['desc'] = desc
        self.__orderby__.append(data)
    
    # setGroupby
    def setGroupby(self, key):
        self.__groupby__.append(key)
        
    def setSearchField(self, **kwargs) :
        self.__searchFields__.append(kwargs)
    
    # getStart
    def getStart(self):
        return (self.page - 1) * self.rowsPerPage
    
    # getRows
    def getRows(self):
        rows = self.getStart() + self.rowsPerPage
        if rows > self.total :
            return self.total - self.getStart()
        else:
            return self.rowsPerPage
        
    #def getStartPage
    def getStartPage(self):
        startPage = int((self.page - 1) / self.showPageNum) * self.showPageNum
        startPage = startPage + 1
        
        return startPage
        
    #def getStopPage
    def getStopPage(self):
        stopPage = self.getStartPage() + self.showPageNum
        if stopPage > self.totalPages :
            stopPage = self.totalPages
            
        return stopPage
        
        
    # getCondition
    def getCondition(self):
        condition = ''
        for data in self.__conditions__ :
            if condition != '' :
                condition = condition + ' ' + data['type'] + ' '
            condition = condition + data['condition']
        return condition
            
    # getResult
    def getResults(self, isEcho=False):
        kwargs = dict()
        kwargs['isEcho'] = isEcho
        
        fields = ''
        for field in self.__fields__ :
            if fields != '' :
                fields = fields + ','
            
            fields = fields + field
            
            if self.__fields__[field] :     
                fields = fields + ' AS ' + self.__fields__[field]
        
        kwargs['field'] = fields
        kwargs['where'] = self.getCondition()
        
        kwargs['groupby'] = ''
        for data in self.__groupby__ :
            if kwargs['groupby'] != '' :
                kwargs['groupby'] = kwargs['groupby'] + ','
            kwargs['groupby'] = kwargs['groupby'] + data

        if kwargs['groupby'] != '' :
            if kwargs['where'] == '' :
                condition = " GROUP BY " + kwargs['groupby']
            else :
                condition = " WHERE " + kwargs['where'] + " GROUP BY " + kwargs['groupby']
                
            kwargs['table'] = "(SELECT %s FROM %s %s) as x" % (fields, self.__tableName__, condition)
            kwargs["where"] = ''
        else :
            kwargs['table'] = self.__tableName__
            
        results = self.__lib__['conn'].select(table=kwargs['table'],field="COUNT(*) AS count",where=kwargs["where"],isEcho=kwargs['isEcho'])
        
        self.total = int(results[0]['count'])
        
        if self.rowsPerPage > 0 :
            self.totalPages = int((self.total - 1) / int(self.rowsPerPage)) + 1;
        else :
            self.totalPages = 1
            
        kwargs['orderby'] = ''
        for data in self.__orderby__ :
            if kwargs['orderby'] != '' :
                kwargs['orderby'] = kwargs['orderby'] + ','
            kwargs['orderby'] = kwargs['orderby'] + data['sort'] + ' ' + data['desc']
                
        #print(self.rowsPerPage)
        #print(self.total)
        
        kwargs['start'] = self.getStart()
        kwargs['rows'] = self.getRows()
        
        if kwargs['groupby'] != '' :
            kwargs['field'] = '*'
            kwargs['groupby'] = ''
            kwargs['orderby'] = ''
            
        self.results = self.__lib__['conn'].select(**kwargs)

        return self.results
    
    # getOnlyResult
    def getOnlyResult(self, start=0, rows=0, isEcho=False):
        kwargs = dict()
        kwargs['isEcho'] = isEcho
        kwargs['table'] = self.__tableName__
        
        fields = ''
        for field in self.__fields__ :
            if fields != '' :
                fields = fields + ','
            
            fields = fields + field
            
            if self.__fields__[field] :     
                fields = fields + ' AS ' + self.__fields__[field]
        
        kwargs['field'] = fields
        kwargs['where'] = self.getCondition()
        
        kwargs['groupby'] = ''
        for data in self.__groupby__ :
            if kwargs['groupby'] != '' :
                kwargs['groupby'] = kwargs['groupby'] + ','
            kwargs['groupby'] = kwargs['groupby'] + data

        kwargs['orderby'] = ''
        for data in self.__orderby__ :
            if kwargs['orderby'] != '' :
                kwargs['orderby'] = kwargs['orderby'] + ','
            kwargs['orderby'] = kwargs['orderby'] + data['sort'] + ' ' + data['desc']
                
        #print(self.rowsPerPage)
        #print(self.total)
        if start :
            kwargs['start'] = start
        if rows :
            kwargs['rows'] = rows
            
        self.results = self.__lib__['conn'].select(**kwargs)
        self.total = len(self.results)
        self.totalPages = 1
        self.page = 1
        self.rowsPerPage = self.total
        
        return self.results
    
    # displayLabel
    def displayLabel(self):
        orderby = self.__orderby__[0]

        tag = ''
        
        tag = tag + '<tr>'
        tag = tag + '\n\t\t\t\t\t'
        if self.isCart :
            tag = tag + '<th><input type="checkbox" name="isAllCart"/></th>'
            tag = tag + '\n\t\t\t\t\t'
        for labels in self.__labels__ :
            tag = tag + '<th>'
            tag = tag + '\n\t\t\t\t\t\t'
            for label in labels :
                for key in label :
                    if label[key] == '' :
                        tag = tag + '<div>%s</div>' % (key)
                    elif orderby['sort'] == label[key] and orderby['desc'] == 'desc' :
                        tag = tag + '<div class="%s"><a href="javascript:$(\'#%s\').setSort(\'%s\', \'%s\')" class="bold">%s ↑</a></div>' % (label[key], self.__formName__, label[key], 'asc', key)
                    elif orderby['sort'] == label[key] and orderby['desc'] == 'asc' :
                        tag = tag + '<div class="%s"><a href="javascript:$(\'#%s\').setSort(\'%s\', \'%s\')" class="bold">%s ↓</a></div>' % (label[key], self.__formName__, label[key], 'desc', key)
                    else :
                        tag = tag + '<div class="%s"><a href="javascript:$(\'#%s\').setSort(\'%s\', \'%s\')">%s ↓</a></div>' % (label[key], self.__formName__, label[key], 'desc', key)
            tag = tag + '\n\t\t\t\t\t'
            tag = tag + '</th>'
            tag = tag + '\n\t\t\t\t\t'
            
        tag = tag + '\n\t\t\t\t'
        tag = tag + '</tr>'

        return tag

    # displayHead
    def displayHead(self):
        tag = '<div id="%sList" class="list">' % self.__formName__
        tag = tag + '\n\t'
        tag = tag + '<form id="%sListForm" action="%s" method="get" class="listForm">' % (self.__formName__, self.__action__)
        tag = tag + '\n\t'
        tag = tag + '<div class="top">'
        tag = tag + '\n\t\t'
        
        if len(self.__searchFields__) :
            tag = tag + '<table class="form">'
        
            for data in self.__searchFields__ :
                tag = tag + '\n\t\t\t'
                tag = tag + '<tr>';
                tag = tag + '\n\t\t\t\t'
                tag = tag + '<th>' + data['name'] + '</th>';
                tag = tag + '<td>' + data['tag'] + '</td>';
                tag = tag + '\n\t\t\t'
                tag = tag + '</tr>';
            
            tag = tag + '</table>'
            tag = tag + '\n\t\t'
        tag = tag + '<div class="search">'
        tag = tag + '\n\t\t\t'
        tag = tag + '<input type="text" name="keyword" value="%s"/>' % self.keyword
        tag = tag + '\n\t\t\t'
        tag = tag + '<input type="submit" value="검색" class="button"/>'
        tag = tag + '\n\t\t\t'
        tag = tag + '<input type="button" id="btnSetup" value="설정" onclick="$(\'#%sSetupDialog\').ELCDialogShow(\'#btnSetup\');" class="button"/>' % self.__formName__
        tag = tag + '\n\t\t'
        tag = tag + '</div>'
        tag = tag + '\n\t\t'
        tag = tag + '<div class="page_setup">'
        tag = tag + '\n\t\t\t'
        tag = tag + '<input type="text" name="page" value="%s"/>' % self.page
        tag = tag + ' / <span class="totalPages">%s</span>' % self.totalPages
        tag = tag + '\n\t\t\t'
        tag = tag + '<a href="javascript:$(\'#%sListForm\').ELCListPrevPage();" class="button">이전</a>' % self.__formName__
        tag = tag + '\n\t\t\t'
        tag = tag + '<a href="javascript:$(\'#%sListForm\').ELCListNextPage();" class="button">다음</a>' % self.__formName__
        tag = tag + '\n\t\t'
        tag = tag + '</div>'
        tag = tag + '\n\t\t'
        tag = tag + '<div id="%sSetupDialog" class="dialog">' % self.__formName__
        tag = tag + '\n\t\t\t'
        tag = tag + '<div class="head">'
        tag = tag + '\n\t\t\t\t'
        tag = tag + '<h1>리스트설정</h1>'
        tag = tag + '<a href="javascript:$(\'#%sSetupDialog\').hide();" class="button">X</a>' % self.__formName__
        tag = tag + '\n\t\t\t'
        tag = tag + '</div>'
        tag = tag + '\n\t\t\t'
        tag = tag + '<div class="body">'
        tag = tag + '\n\t\t\t\t'
        tag = tag + '<table class="form">'
        tag = tag + '\n\t\t\t\t\t'
        tag = tag + '<tr>'
        tag = tag + '\n\t\t\t\t\t\t'
        tag = tag + '<th>정렬기준</th>'
        tag = tag + '\n\t\t\t\t\t\t'
        tag = tag + '<td>'
        tag = tag + '\n\t\t\t\t\t\t\t'
        tag = tag + '<select name="sort">'
        
        orderby = self.__orderby__[0]

        for labels in self.__labels__ :
            for label in labels :
                for key in label :
                    if orderby['sort'] == label[key] :
                        tag = tag + '<option value="%s" selected="selected" style="background:#EEEEEE;">%s</option>' % (label[key], key)
                    else :
                        tag = tag + '<option value="%s">%s</option>' % (label[key], key)
       
        tag = tag + '</select>'
        tag = tag + '\n\t\t\t\t\t\t'
        tag = tag + '</td>'
        tag = tag + '\n\t\t\t\t\t'
        tag = tag + '</tr>'
        tag = tag + '\n\t\t\t\t\t'
        tag = tag + '<tr>'
        tag = tag + '\n\t\t\t\t\t\t'
        tag = tag + '<th>정렬방식</th>'
        tag = tag + '\n\t\t\t\t\t\t'
        tag = tag + '<td>'
        tag = tag + '\n\t\t\t\t\t\t\t'
        tag = tag + '<select name="desc">'
        tag = tag + '<option value="asc"'
        if orderby['desc'] != 'desc' :
            tag = tag + ' checked="checked"'
        tag = tag + '>정순</option>'
        tag = tag + '<option value="desc"'
        if orderby['desc'] == 'desc' :
            tag = tag + ' selected="selected" style="background:#EEEEEE;"'
        tag = tag + '>역순</option>'
        tag = tag + '</select>'
        tag = tag + '\n\t\t\t\t\t\t'
        tag = tag + '</td>'
        tag = tag + '\n\t\t\t\t\t'
        tag = tag + '</tr>'
        tag = tag + '\n\t\t\t\t\t'
        tag = tag + '<tr>'
        tag = tag + '\n\t\t\t\t\t\t'
        tag = tag + '<th>페이지당줄수</th>'
        tag = tag + '\n\t\t\t\t\t\t'
        tag = tag + '<td>'
        tag = tag + '\n\t\t\t\t\t\t\t'
        tag = tag + '<input type="text" name="rowsPerPage" value="%s"/> <a href="javascript:$(\'#%sListForm input[name=rowsPerPage]\').val(\'%s\');" class="button">전체</a>' % (self.rowsPerPage, self.__formName__, self.total)
        tag = tag + '\n\t\t\t\t\t\t'
        tag = tag + '</td>'
        tag = tag + '\n\t\t\t\t\t'
        tag = tag + '</tr>'
        tag = tag + '\n\t\t\t\t'
        tag = tag + '</table>'
        tag = tag + '\n\t\t\t'
        tag = tag + '</div>'
        tag = tag + '\n\t\t\t'
        tag = tag + '<div class="foot">'
        tag = tag + '\n\t\t\t\t'
        tag = tag + '<input type="submit" value="적용" class="button">'
        tag = tag + '\n\t\t\t'
        tag = tag + '</div>'
        tag = tag + '\n\t\t'
        tag = tag + '</div>'
        tag = tag + '\n\t'
        tag = tag + '</div>'
        tag = tag + '\n\t'
        tag = tag + '<div class="middle">'
        tag = tag + '\n\t\t'
        tag = tag + '<table class="list">'
        tag = tag + '\n\t\t\t'
        tag = tag + '<thead>'
        tag = tag + '\n\t\t\t\t'
        tag = tag + self.displayLabel()
        tag = tag + '\n\t\t\t'
        tag = tag + '</thead>'
        tag = tag + '\n\t\t\t'
        
        return tag
    
    # displayFoot
    def displayFoot(self):
        tag = '\n\t\t\t'
        tag = tag + '<tfoot>'
        tag = tag + '\n\t\t\t'
        tag = tag + '</tfoot>'
        tag = tag + '\n\t\t'
        tag = tag + '</table>'
        tag = tag + '\n\t'
        tag = tag + '</div>'
        tag = tag + '\n\t'
        tag = tag + '<div class="bottom">'
        tag = tag + '\n\t\t'
        tag = tag + '<div class="buttons">'
        tag = tag + '\n\t\t\t'
       
        for button in self.__buttons__ :
            tag = tag + '<a'
            if 'id' in button :
                tag = tag + ' id="' + button['id'] + '"'
            
            if 'href' in button :
                tag = tag + ' href="' + button['href'] + '"'
                
            if 'target' in button :
                tag = tag + ' target="' + button['target'] + '"'
                
            if 'class' in button :
                tag = tag + ' class="button ' + button['class'] + '"'
            else :
                tag = tag + ' class="button"'
                
            if 'option' in button :
                tag = tag + ' ' + button['option']
                
            tag = tag + '>' + button['name'] + '</a>'
                
        tag = tag + '\n\t\t'
        tag = tag + '</div>'
        tag = tag + '\n\t\t'
        tag = tag + '<div class="paging">'
        tag = tag + '\n\t\t\t'
        tag = tag + self.displayPaging()
        tag = tag + '\n\t\t'
        tag = tag + '</div>'
        tag = tag + '\n\t'
        tag = tag + '</div>'
        tag = tag + '\n\t'
        tag = tag + '</form>'
        tag = tag + '\n'
        tag = tag + '</div>'
        tag = tag + '\n'
        
        return tag
    
    # displayPaging
    def displayPaging(self):
        tag = ''
        if self.page != 1:
            tag = tag + '<a href="javascript:$(\'#%sListForm\').ELCListMovePage(1);" class="firstPage">&lt;&lt;</a>' % self.__formName__
            tag = tag + '<a href="javascript:$(\'#%sListForm\').ELCListMovePage(%s);" class="prevPage">&lt;</a>' % (self.__formName__, self.page - 1)
        
        for iPage in range(self.getStartPage(), self.getStopPage() + 1) :
            if iPage == self.page :
                tag = tag + '<b>%s</b>' % iPage
            else :
                tag = tag + '<a href="javascript:$(\'#%sListForm\').ELCListMovePage(%s);">%s</a>' % (self.__formName__, iPage, iPage)
                
        if self.page != self.totalPages:
            tag = tag + '<a href="javascript:$(\'#%sListForm\').ELCListMovePage(%s);" class="nextPage">&gt;</a>' % (self.__formName__, self.page + 1)
            tag = tag + '<a href="javascript:$(\'#%sListForm\').ELCListMovePage(%s);" class="lastPage">&gt;&gt;</a>' % (self.__formName__, self.totalPages)
            
        return tag
