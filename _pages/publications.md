---
layout: page
permalink: /publications/
title: publications
description: Publications split into arXiv preprints and accepted papers.
nav: true
nav_order: 2
---

{% include bib_search.liquid %}

<p>* indicates equal contribution and † indicates corresponding author.</p>

<div class="publications">
  <h2>arXiv Preprints</h2>
  {% bibliography --group_by none --sort_by year,month --order descending --query @*[status=preprint]* %}

  <h2>Accepted Papers</h2>
  {% bibliography --group_by none --sort_by year,month --order ascending --query @*[status=accepted]* %}
</div>
