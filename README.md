# gmapIcons2osmand
<div align="center">
  
![python](https://img.shields.io/badge/python-green?logo=python)
![osmand](https://img.shields.io/badge/osmand%20layer-GPX-navy?logo=osmand)
![License](https://img.shields.io/badge/license-MIT-blue)
<a href="https://mariush444.github.io/gmapIcons2osmand/kmz2osmand-online.html"><img src="https://img.shields.io/badge/On&ndash;line-A155E8"></a>

</div>

Conversion of KMZ files to GPX format for OsmAnd but with icons.

OsmAnd supports importing KMZ files, but all icons are converted into a default red star. This happens because OsmAnd does not support Google Maps (Gmail-style) icons.

It looks at each original icon and assigns the most similar equivalent from OsmAnd’s icon set, preserving as much visual meaning as possible.

Proposition of mapping between gmap and OsmAnd icons can be found in <a href="https://mariush444.github.io/gmapIcons2osmand/icons-gmap-osmand.pdf">icons-gmap-osmand.pdf</a><br>
Example of result:
<!-- ![icons](https://user-images.githubusercontent.com/66887280/165990415-8bcc363a-6e71-425d-b6db-90f6ed753c1f.png) -->
<img width="692" height="646" alt="kmz2osmand" src="https://github.com/user-attachments/assets/ea85a2e6-4f33-4d5c-801f-575e9d94fc24" />

Project is based on https://www.mail-archive.com/osmand@googlegroups.com/msg07817.html

<!-- Current icons list https://mariush444.github.io/gmapIcons2osmand/icons-current.html -->
<a href="https://mariush444.github.io/gmapIcons2osmand/kmz2osmand-online.html">NEW - Online converter</a>

PS</br>
Python 3 is needed.</br>
There are some icons for my needs only implemented at this moment.</br>
Any icons that can’t be matched are shown as a black question mark in OsmAnd, making it easy to spot them and decide what to do next.</br>
Let me know if you have suggestions or don't know how to do it.</br>

<!--
If you like it you can buy me <a href="https://buy.stripe.com/5kA5nP7B27OQdFK7sv"> 🍷 </a> or <a href="https://buy.stripe.com/5kA6rTcVm8SUeJOeUW"> ☕ </a>
-->
