// Scroll progress bar
(function() {
    const bar = document.createElement('div');
    bar.className = 'scroll-progress';
    document.body.prepend(bar);

    window.addEventListener('scroll', function() {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.width = (scrollTop / docHeight * 100) + '%';
    }, { passive: true });
})();

// ToC active state
(function() {
    const toc = document.querySelector('.toc');
    if (!toc) return;

    const links = toc.querySelectorAll('a[href^="#"]');
    const sections = [];

    links.forEach(link => {
        const id = link.getAttribute('href').substring(1);
        const section = document.getElementById(id);
        if (section) sections.push({ link, section });
    });

    function updateActive() {
        const scrollPos = window.scrollY + 150;
        let current = sections[0];

        for (const s of sections) {
            if (s.section.offsetTop <= scrollPos) {
                current = s;
            }
        }

        links.forEach(l => l.classList.remove('active'));
        if (current) current.link.classList.add('active');
    }

    window.addEventListener('scroll', updateActive, { passive: true });
    updateActive();
})();
