<!-- ---
layout: default
title: AI Consulting
--- -->

<div class="content-section">
    <h1>AI Consulting</h1>

    <p>Is your business using AI but are feeling stuck? My clients often feel overwhelmed navigating the sea of options and trade-offs when rolling out AI and often just want to know if they're doing it right.</p>

    <p>As a hands-on AI architect, I show where you're doing great, as well as provide actionable feedback on where you can improve as well as give ideas on where you can go next. I have 17+ years of experience in software engineering, architecture and management, as well as 6+ years producing and operating AI/ML applications.</p>

    <ul>
        <li><strong>AI architecture</strong> — RAG, knowledge graphs, vector databases, etc.</li>
        <li><strong>AI/ML Operations</strong> — Deploying, testing, and monitoring AI or ML apps.</li>
        <li><strong>Rollout</strong> — ChatGPT or Microsoft Copilot</li>
        <li><strong>Engineering</strong> — Using AI code generation tools effectively</li>
        <li><strong>Education</strong> — Programs that enable employees to get the most from AI</li>
    </ul>

    <p>Interested? <a href="/contact">Contact me</a> for a first consultation. I prefer longer-term engagements that go beyond initial advice.</p>

    <a href="/contact" class="contact-button">Contact Me</a>
</div>

<div class="content-section">
    <h2>Relevant Articles</h2>
    {% for post in site.posts %}
      {% if post.categories contains "consulting" and post.is_draft != true %}
        <div class="post-item">
            <a href="{{ post.url }}" class="title">{{ post.title }}</a>
            <div class="excerpt">{{ post.summary or post.excerpt }}</div>
        </div>
      {% endif %}
    {% endfor %}
</div>
