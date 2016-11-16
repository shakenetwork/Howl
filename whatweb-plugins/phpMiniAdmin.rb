
##
# This file is part of WhatWeb and may be subject to
# redistribution and commercial restrictions. Please see the WhatWeb
# web site for more information on licensing and terms of use.
# http://www.morningstarsecurity.com/research/whatweb
#
Plugin.define "phpMiniAdmin" do
author "orange"
description "phpminiadmin - extremely lightweight alternative to heavy phpMyAdmin for quick and easy access MySQL databases."
website "http://phpminiadmin.sourceforge.net/"

# This is the matches array. 
# Each match is treated independently.

# Matches #
matches [

# This searches for a text string.
{ :text => '<title>phpMiniAdmin<\/title>' },

# This searches for a regular expression. Note that the slashes are escaped.
{ :regexp => /<title>phpMiniAdmin<\/title>/ },

# This extracts the version of Generic CMS from the Mega generator tag.
{ :version => /target="_blank"><b>(.*?)<\/b><\/a>/ }, 

] 

end