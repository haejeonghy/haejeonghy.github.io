---
layout  : wikiindex
title   : blog index
toc     : false
public  : true
comment : false
updated : 2026-03-08 16:00:00 +0900
regenerate: true
---

## blog posts
<div>
    <ul>
{% for post in site.posts %}
    {% if post.public == true %}
        <li>
            <a class="post-link" href="{{ post.url | prepend: site.baseurl }}">
                {{ post.title }}
            </a>
        </li>
    {% endif %}
{% endfor %}
    </ul>
</div>
