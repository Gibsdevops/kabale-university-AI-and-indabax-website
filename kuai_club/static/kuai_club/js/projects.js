// Optimized Projects Slider with Performance Improvements
document.addEventListener('DOMContentLoaded', function () {
  console.log('Projects slider initializing...');

  // Cache DOM elements
  const sliderWrapper = document.getElementById('projectsSliderWrapper');
  const slider = document.getElementById('projectsSlider');
  const btnLeft = document.getElementById('slideLeft');
  const btnRight = document.getElementById('slideRight');

  // Early return if elements not found
  if (!sliderWrapper || !slider || !btnLeft || !btnRight) {
    console.error('Required elements not found!');
    return;
  }

  // Configuration constants
  const CONFIG = {
    cardWidth: 350,
    gap: 30,
    scrollAmount: 380, // cardWidth + gap
    maxDepth: 5,
    scrollDebounce: 100, // Reduced from 200ms
    animationDelay: 200, // Reduced from 300ms
    fetchTimeout: 8000 // 8 second timeout
  };

  // State management
  const state = {
    currentPage: 1,
    loading: false,
    hasNextPage: true,
    loadedProjectIds: new Set(),
    scrollTimeout: null,
    lastScrollTime: 0
  };

  // Initialize loaded project IDs from existing cards
  function initializeLoadedIds() {
    const existingCards = slider.querySelectorAll('.project-card[data-project-id]');
    existingCards.forEach(card => {
      const projectId = card.getAttribute('data-project-id');
      if (projectId) state.loadedProjectIds.add(projectId);
    });
  }

  // Optimized HTML escaping using a reusable element
  const tempDiv = document.createElement('div');
  function escapeHtml(text) {
    tempDiv.textContent = text;
    return tempDiv.innerHTML;
  }

  // Optimized project card creation with fragment
  function createProjectCard(project) {
    if (state.loadedProjectIds.has(project.id.toString())) return null;

    const card = document.createElement('div');
    card.className = 'project-card';
    card.setAttribute('data-project-id', project.id);

    // Optimize image loading
    const imgSrc = project.image_url || '{% static "images/default-project.jpg" %}';
    
    // Optimize date formatting (cache locale)
    const formattedDate = new Date(project.publish_date).toLocaleDateString('en-US', {
      year: 'numeric', 
      month: 'long', 
      day: 'numeric'
    });

    // Optimize summary truncation
    const summary = project.summary.length > 100 
      ? project.summary.substring(0, 100) + '...' 
      : project.summary;

    // Use template literal for better performance
    card.innerHTML = `
      <img src="${imgSrc}" 
           alt="${escapeHtml(project.title)}" 
           class="project-image" 
           loading="lazy" 
           decoding="async" />
      <div class="project-content">
        <h3 class="project-title">${escapeHtml(project.title)}</h3>
        <p class="project-summary">${escapeHtml(summary)}</p>
        <div class="project-meta">
          <span class="project-date">${formattedDate}</span>
          ${project.url ? `<a href="${escapeHtml(project.url)}" class="project-link" target="_blank" rel="noopener">Learn More</a>` : ''}
        </div>
      </div>
    `;

    state.loadedProjectIds.add(project.id.toString());
    return card;
  }

  // Optimized loading card management
  let loadingCard = null;
  function showLoadingCard() {
    if (loadingCard) return; // Don't create multiple loading cards
    
    loadingCard = document.createElement('div');
    loadingCard.className = 'project-card loading-card';
    loadingCard.innerHTML = '<div class="loading-spinner">Loading...</div>';
    slider.appendChild(loadingCard);
  }

  function removeLoadingCard() {
    if (loadingCard && loadingCard.parentNode) {
      loadingCard.parentNode.removeChild(loadingCard);
      loadingCard = null;
    }
  }

  // Optimized mid-card highlighting with cached calculations
  function updateMidCardHighlight() {
    const cards = slider.querySelectorAll('.project-card:not(.loading-card)');
    
    // Remove all mid-card classes first
    cards.forEach(card => card.classList.remove('mid-card'));

    // Get wrapper bounds once
    const wrapperRect = sliderWrapper.getBoundingClientRect();
    const visibleCards = [];

    // Filter visible cards more efficiently
    for (let i = 0; i < cards.length; i++) {
      const rect = cards[i].getBoundingClientRect();
      if (rect.left >= wrapperRect.left && rect.right <= wrapperRect.right) {
        visibleCards.push(cards[i]);
      }
    }

    // Highlight middle card if we have 3+ visible cards
    if (visibleCards.length >= 3) {
      visibleCards[1].classList.add('mid-card');
    }
  }

  // Optimized fetch with timeout and better error handling
  async function fetchProjects(page, maxDepth = CONFIG.maxDepth) {
    if (state.loading || !state.hasNextPage || page > maxDepth) return false;

    state.loading = true;
    btnRight.disabled = true;
    showLoadingCard();

    // Create abort controller for timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), CONFIG.fetchTimeout);

    try {
      const response = await fetch(`/api/projects/?page=${page}`, {
        signal: controller.signal,
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.projects && data.projects.length > 0) {
        let newProjectsAdded = 0;
        const fragment = document.createDocumentFragment();

        // Use document fragment for better performance
        data.projects.forEach(proj => {
          const card = createProjectCard(proj);
          if (card) {
            fragment.appendChild(card);
            newProjectsAdded++;
          }
        });

        // Append all cards at once
        if (fragment.children.length > 0) {
          slider.appendChild(fragment);
        }

        state.hasNextPage = data.has_next;

        // Recursive call optimization
        if (newProjectsAdded === 0 && state.hasNextPage && page < maxDepth) {
          state.currentPage++;
          return await fetchProjects(state.currentPage, maxDepth);
        }

        // Defer UI updates to next frame
        requestAnimationFrame(() => {
          updateMidCardHighlight();
        });

        return newProjectsAdded > 0;
      } else {
        state.hasNextPage = false;
        return false;
      }
    } catch (error) {
      clearTimeout(timeoutId);
      console.error('Error fetching projects:', error);
      state.hasNextPage = false;
      return false;
    } finally {
      state.loading = false;
      removeLoadingCard();
      btnRight.disabled = false;
      btnRight.innerHTML = '<i class="fas fa-chevron-right"></i>';
    }
  }

  // Optimized button state updates
  function updateButtonStates() {
    const scrollLeft = sliderWrapper.scrollLeft;
    const maxScroll = sliderWrapper.scrollWidth - sliderWrapper.clientWidth;

    btnLeft.disabled = scrollLeft <= 0;
    btnRight.disabled = state.loading || (!state.hasNextPage && scrollLeft >= maxScroll - 10);
  }

  // Optimized scroll handling with requestAnimationFrame
  function handleScroll() {
    if (state.scrollTimeout) return;
    
    state.scrollTimeout = requestAnimationFrame(() => {
      updateButtonStates();
      updateMidCardHighlight();
      state.scrollTimeout = null;
    });
  }

  // Throttled scroll event
  let lastScrollTime = 0;
  sliderWrapper.addEventListener('scroll', () => {
    const now = Date.now();
    if (now - lastScrollTime > CONFIG.scrollDebounce) {
      lastScrollTime = now;
      handleScroll();
    }
  }, { passive: true });

  // Optimized button click handlers
  btnLeft.addEventListener('click', function (e) {
    e.preventDefault();
    if (state.loading) return;

    const currentScroll = sliderWrapper.scrollLeft;
    const newScroll = Math.max(0, currentScroll - CONFIG.scrollAmount);

    sliderWrapper.scrollTo({ left: newScroll, behavior: 'smooth' });

    // Use requestAnimationFrame for UI updates
    setTimeout(() => {
      requestAnimationFrame(() => {
        updateButtonStates();
        updateMidCardHighlight();
      });
    }, CONFIG.animationDelay);
  });

  btnRight.addEventListener('click', async function (e) {
    e.preventDefault();
    if (state.loading) return;

    const currentScroll = sliderWrapper.scrollLeft;
    const maxScroll = sliderWrapper.scrollWidth - sliderWrapper.clientWidth;

    if (currentScroll >= maxScroll - CONFIG.scrollAmount && state.hasNextPage && !state.loading) {
      state.currentPage++;
      const loaded = await fetchProjects(state.currentPage);

      if (loaded) {
        setTimeout(() => {
          const newMaxScroll = sliderWrapper.scrollWidth - sliderWrapper.clientWidth;
          const newScroll = Math.min(newMaxScroll, currentScroll + CONFIG.scrollAmount);
          sliderWrapper.scrollTo({ left: newScroll, behavior: 'smooth' });

          setTimeout(() => {
            requestAnimationFrame(() => {
              updateButtonStates();
              updateMidCardHighlight();
            });
          }, CONFIG.animationDelay);
        }, 100);
      }
    } else {
      const newScroll = Math.min(maxScroll, currentScroll + CONFIG.scrollAmount);
      sliderWrapper.scrollTo({ left: newScroll, behavior: 'smooth' });

      setTimeout(() => {
        requestAnimationFrame(() => {
          updateButtonStates();
          updateMidCardHighlight();
        });
      }, CONFIG.animationDelay);
    }
  });

  // Cleanup function for when page unloads
  window.addEventListener('beforeunload', () => {
    if (state.scrollTimeout) {
      cancelAnimationFrame(state.scrollTimeout);
    }
  });

  // Initialize
  initializeLoadedIds();
  requestAnimationFrame(() => {
    updateButtonStates();
    updateMidCardHighlight();
  });
});