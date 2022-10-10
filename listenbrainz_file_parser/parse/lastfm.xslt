<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"   xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<scrobbles>
<xsl:for-each select="/scrobbles/track">
<track>
<artist>
<xsl:value-of   select="./artist"/>
</artist>
<artist_mbid>
<xsl:value-of   select="./artist/@mbid"/>
</artist_mbid>
<name>
<xsl:value-of   select="./name"/>
</name>
<track_mbid>
<xsl:value-of   select="./mbid"/>
</track_mbid>
<album>
<xsl:value-of   select="./album"/>
</album>
<album_mbid>
<xsl:value-of   select="./album/@mbid"/>
</album_mbid>
<url>
<xsl:value-of   select="./url"/>
</url>
<utc>
<xsl:value-of   select="./date/@uts"/>
</utc>
</track>
</xsl:for-each>
</scrobbles>
</xsl:template>
</xsl:stylesheet>