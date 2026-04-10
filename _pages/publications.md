---
layout: page
permalink: /publications/
title: publications
description: Publications ordered by preprint status and release time.
nav: true
nav_order: 2
---

{% include bib_search.liquid %}

<p>* indicates equal contribution and † indicates corresponding author.</p>

<div class="publications">
  {% bibliography --group_by none --sort_by year,month --order descending --query @*[status=preprint]* %}
  {% bibliography --group_by none --sort_by year,month --order descending --query @*[status=accepted]* %}
</div>
