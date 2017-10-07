
from urllib import request
from lxml import etree
import time

xslt_root = etree.XML("""\
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" >
<xsl:template match="/">
<列表>
<xsl:apply-templates select="//*[@id='forum' and count(./table/tbody/tr[position()>=1 and count(.//*[@class='topic']/a/text())>0])>0]" mode="列表"/>
</列表>
</xsl:template>



<xsl:template match="table/tbody/tr[position()>=1]" mode="list">
<item>
<标题>
<xsl:value-of select="*//*[@class='topic']/a/text()"/>
<xsl:value-of select="*[@class='topic']/a/text()"/>
<xsl:if test="@class='topic'">
<xsl:value-of select="a/text()"/>
</xsl:if>
</标题>
<回复数>
<xsl:value-of select="*//*[@class='replies']/text()"/>
<xsl:value-of select="*[@class='replies']/text()"/>
<xsl:if test="@class='replies'">
<xsl:value-of select="text()"/>
</xsl:if>
</回复数>
</item>
</xsl:template>

<xsl:template match="//*[@id='forum' and count(./table/tbody/tr[position()>=1 and count(.//*[@class='topic']/a/text())>0])>0]" mode="列表">
<item>
<list>
<xsl:apply-templates select="table/tbody/tr[position()>=1]" mode="list"/>
</list>
</item>
</xsl:template>
</xsl:stylesheet>""")

baseurl = "http://www.gooseeker.com/cn/forum/7"
basefilebegin = "jsk_bbs_"
basefileend = ".xml"
count = 1
while (count < 12):
        url = baseurl + "?page=" + str(count)
        conn = request.urlopen(url)
        doc = etree.HTML(conn.read())
        transform = etree.XSLT(xslt_root)
        result_tree = transform(doc)
        print(str(result_tree))
        file_obj = open(basefilebegin+str(count)+basefileend,'w',encoding='UTF-8')
        file_obj.write(str(result_tree))
        file_obj.close()
        count += 1
        time.sleep(2)