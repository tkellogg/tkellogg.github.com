
<section class="content-section">
    <h2>Full Time</h2>
    <p>I'm currently open to full time positions within AI engineering. I'm flexible in regards
    to title and role, the important part to me is that I'm contributing to AI in a way that enables others
    to <a href="/blog/2025/01/02/normware.html">solve their own problems</a>.</p>

    <p>I have <a href="http://www.linkedin.com/pub/tim-kellogg/13/29/698">experience</a> in management, 
    product and as a staff+ engineer. Location should be remote or Raleigh/Durham
    area, either is fine but I'm not open to moving.</p>

    <p>
    See my <a href="/Resume-TimKellogg.pdf">resume</a> for more info.
    </p>

    <a href="/contact" class="contact-button">Contact Me</a>
</section>
<section class="content-section">
    <h2>AI Consulting</h2>

    <p>
    I help people <a href="/blog/2025/01/02/normware.html">solve their own problems</a>. A lot of it is
    education, some of it is targeting the right personalities and investing in enabling them though
    technology.
    </p>

    <p>
    I also help navigate technological challenges. As an experienced software architect and engineer,
    I help clients navigate the tumultuous changes in the AI field.
    </p>


    <p>Interested? <a href="/contact">Contact me</a> for a free first consultation.</p>

    <a href="/contact" class="contact-button">Contact Me</a>
</section>

<div class="content-section">
    <h2>Related Articles</h2>
    {% for post in site.posts %}
      {% if post.categories contains "consulting" and post.is_draft != true %}
        <div class="post-item">
            <a href="{{ post.url }}" class="title">{{ post.title }}</a>
       {% if post.summary %}
            <div class="excerpt">{{ post.summary }}</div>
       {% else %}
            <div class="excerpt">{{ post.excerpt }}</div> 
       {% endif %}
        </div>
      {% endif %}
    {% endfor %}
</div>
